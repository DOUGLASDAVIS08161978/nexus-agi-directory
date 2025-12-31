"""Health monitoring worker for Nexus Watcher daemon."""

import json
import asyncio
import aiohttp
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .base_worker import BaseWorker
from ..database.models import APIHealthRecord, APIStatus
from ..utils.helpers import timestamp_iso


class HealthMonitorWorker(BaseWorker):
    """Worker that monitors health of all APIs in the directory."""

    def __init__(self, *args, **kwargs):
        super().__init__("health_monitor", *args, **kwargs)
        self._apis: List[Dict[str, Any]] = []
        self._consecutive_failures: Dict[str, int] = {}

    async def _load_directory(self):
        """Load APIs from the directory file."""
        directory_file = Path(self.config.get('directory.source_file'))

        if not directory_file.exists():
            self.logger.error(f"Directory file not found: {directory_file}")
            return

        try:
            with open(directory_file, 'r') as f:
                data = json.load(f)
                # Handle both array format and object format
                if isinstance(data, list):
                    self._apis = data
                else:
                    self._apis = data.get('services', [])
                self.logger.info(f"Loaded {len(self._apis)} APIs from directory")
        except Exception as e:
            self.logger.error(f"Failed to load directory: {e}")

    async def _check_api_health(
        self,
        session: aiohttp.ClientSession,
        api: Dict[str, Any]
    ) -> APIHealthRecord:
        """
        Check health of a single API.

        Args:
            session: aiohttp session
            api: API data from directory

        Returns:
            Health record
        """
        api_id = api.get('id', 'unknown')
        endpoint = api.get('endpoint', '')

        if not endpoint:
            return APIHealthRecord(
                api_id=api_id,
                endpoint='',
                status=APIStatus.ERROR.value,
                response_time_ms=None,
                status_code=None,
                error_message="No endpoint defined",
                checked_at=timestamp_iso(),
                consecutive_failures=self._consecutive_failures.get(api_id, 0)
            )

        timeout = self.config.get('health_monitor.timeout', 10)
        max_retries = self.config.get('health_monitor.retry_attempts', 2)

        for attempt in range(max_retries + 1):
            try:
                start_time = datetime.utcnow()

                # Determine HTTP method (HEAD is faster, but some APIs don't support it)
                method = 'HEAD'
                if attempt > 0:  # Retry with GET if HEAD fails
                    method = 'GET'

                async with session.request(
                    method,
                    endpoint,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    allow_redirects=True
                ) as response:
                    response_time = (datetime.utcnow() - start_time).total_seconds() * 1000

                    # Determine status based on HTTP status code
                    if 200 <= response.status < 300:
                        status = APIStatus.HEALTHY.value
                        self._consecutive_failures[api_id] = 0
                    elif 300 <= response.status < 500:
                        status = APIStatus.DEGRADED.value
                        self._consecutive_failures[api_id] = self._consecutive_failures.get(api_id, 0) + 1
                    else:
                        status = APIStatus.DOWN.value
                        self._consecutive_failures[api_id] = self._consecutive_failures.get(api_id, 0) + 1

                    return APIHealthRecord(
                        api_id=api_id,
                        endpoint=endpoint,
                        status=status,
                        response_time_ms=response_time,
                        status_code=response.status,
                        error_message=None,
                        checked_at=timestamp_iso(),
                        consecutive_failures=self._consecutive_failures.get(api_id, 0)
                    )

            except asyncio.TimeoutError:
                if attempt < max_retries:
                    continue
                self._consecutive_failures[api_id] = self._consecutive_failures.get(api_id, 0) + 1
                return APIHealthRecord(
                    api_id=api_id,
                    endpoint=endpoint,
                    status=APIStatus.DOWN.value,
                    response_time_ms=None,
                    status_code=None,
                    error_message="Request timeout",
                    checked_at=timestamp_iso(),
                    consecutive_failures=self._consecutive_failures[api_id]
                )

            except Exception as e:
                if attempt < max_retries:
                    continue
                self._consecutive_failures[api_id] = self._consecutive_failures.get(api_id, 0) + 1
                return APIHealthRecord(
                    api_id=api_id,
                    endpoint=endpoint,
                    status=APIStatus.ERROR.value,
                    response_time_ms=None,
                    status_code=None,
                    error_message=str(e),
                    checked_at=timestamp_iso(),
                    consecutive_failures=self._consecutive_failures[api_id]
                )

    async def run_iteration(self):
        """Execute one health check iteration."""
        # Reload directory
        await self._load_directory()

        if not self._apis:
            self.logger.warning("No APIs to check")
            return

        max_concurrent = self.config.get('health_monitor.max_concurrent', 20)
        semaphore = asyncio.Semaphore(max_concurrent)

        async def check_with_semaphore(session, api):
            async with semaphore:
                return await self._check_api_health(session, api)

        # Create aiohttp session
        connector = aiohttp.TCPConnector(limit=max_concurrent)
        timeout = aiohttp.ClientTimeout(total=self.config.get('health_monitor.timeout', 10))

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Check all APIs concurrently
            tasks = [check_with_semaphore(session, api) for api in self._apis]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Save results to database
            healthy = 0
            degraded = 0
            down = 0
            errors = 0

            for result in results:
                if isinstance(result, Exception):
                    self.logger.error(f"Health check error: {result}")
                    errors += 1
                    continue

                # Save to database
                await self.db.save_health_record(result)

                # Track stats
                if result.status == APIStatus.HEALTHY.value:
                    healthy += 1
                elif result.status == APIStatus.DEGRADED.value:
                    degraded += 1
                elif result.status == APIStatus.DOWN.value:
                    down += 1
                else:
                    errors += 1

                # Log failures
                failure_threshold = self.config.get('health_monitor.failure_threshold', 3)
                if result.consecutive_failures >= failure_threshold:
                    self.logger.warning(
                        f"API {result.api_id} has failed {result.consecutive_failures} "
                        f"consecutive checks (status: {result.status})"
                    )

        self.logger.info(
            f"Health check complete: {healthy} healthy, {degraded} degraded, "
            f"{down} down, {errors} errors (total: {len(self._apis)})"
        )

        # Update stats in database
        await self.db.set_state('last_health_check', timestamp_iso())
        await self.db.set_state('total_apis_monitored', len(self._apis))

    def get_interval(self) -> int:
        """Get check interval from config."""
        return self.config.get('health_monitor.check_interval', 600)
