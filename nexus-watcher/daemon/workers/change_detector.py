"""Change detector worker for monitoring API changes."""

import json
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_worker import BaseWorker
from ..database.models import APIChangeEvent
from ..utils.helpers import timestamp_iso, calculate_hash
from pathlib import Path


class ChangeDetectorWorker(BaseWorker):
    """Worker that detects changes in APIs."""

    def __init__(self, *args, **kwargs):
        super().__init__("change_detector", *args, **kwargs)
        self._apis: List[Dict[str, Any]] = []

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
        except Exception as e:
            self.logger.error(f"Failed to load directory: {e}")

    async def _detect_api_changes(self, api: Dict[str, Any]) -> List[APIChangeEvent]:
        """
        Detect changes for a single API.

        Args:
            api: API data

        Returns:
            List of detected changes
        """
        changes = []
        api_id = api.get('id', 'unknown')

        # Get latest snapshot
        latest_snapshot = await self.db.get_latest_snapshot(api_id)

        # Create current snapshot
        snapshot_data = {
            'endpoint': api.get('endpoint', ''),
            'name': api.get('name', ''),
            'capabilities': api.get('capabilities', []),
            'auth': api.get('auth', {}),
            'status': api.get('status', ''),
            'docs': api.get('docs', ''),
            'version': api.get('version', ''),
        }

        current_hash = calculate_hash(snapshot_data)

        # If no previous snapshot, create one and return
        if not latest_snapshot:
            await self.db.save_api_snapshot(api_id, snapshot_data, current_hash)
            self.logger.debug(f"Created initial snapshot for {api_id}")
            return changes

        # Compare with previous snapshot
        if current_hash != latest_snapshot['hash']:
            previous_data = latest_snapshot['data']

            # Detect specific changes
            for field in ['endpoint', 'name', 'status', 'docs', 'version']:
                old_value = previous_data.get(field, '')
                new_value = snapshot_data.get(field, '')

                if old_value != new_value:
                    # Determine severity
                    severity = self._determine_severity(field, old_value, new_value)

                    change = APIChangeEvent(
                        api_id=api_id,
                        change_type=field,
                        old_value=str(old_value),
                        new_value=str(new_value),
                        detected_at=timestamp_iso(),
                        severity=severity,
                        metadata={'field': field}
                    )
                    changes.append(change)

            # Check auth changes
            old_auth = previous_data.get('auth', {})
            new_auth = snapshot_data.get('auth', {})
            if old_auth != new_auth:
                change = APIChangeEvent(
                    api_id=api_id,
                    change_type='auth',
                    old_value=json.dumps(old_auth),
                    new_value=json.dumps(new_auth),
                    detected_at=timestamp_iso(),
                    severity='high',
                    metadata={'auth_change': True}
                )
                changes.append(change)

            # Check capabilities changes
            old_caps = set(previous_data.get('capabilities', []))
            new_caps = set(snapshot_data.get('capabilities', []))

            if old_caps != new_caps:
                added = list(new_caps - old_caps)
                removed = list(old_caps - new_caps)

                change = APIChangeEvent(
                    api_id=api_id,
                    change_type='capabilities',
                    old_value=json.dumps(list(old_caps)),
                    new_value=json.dumps(list(new_caps)),
                    detected_at=timestamp_iso(),
                    severity='medium',
                    metadata={
                        'added': added,
                        'removed': removed
                    }
                )
                changes.append(change)

            # Save new snapshot
            await self.db.save_api_snapshot(api_id, snapshot_data, current_hash)

        return changes

    def _determine_severity(self, field: str, old_value: Any, new_value: Any) -> str:
        """
        Determine severity of a change.

        Args:
            field: Changed field name
            old_value: Old value
            new_value: New value

        Returns:
            Severity level: 'low', 'medium', 'high', 'critical'
        """
        # Endpoint changes are critical
        if field == 'endpoint':
            return 'critical'

        # Status changes are high severity
        if field == 'status':
            # Downgrade is more severe
            if old_value in ['stable', 'production'] and new_value in ['deprecated', 'beta', 'alpha']:
                return 'high'
            return 'medium'

        # Version changes are medium
        if field == 'version':
            return 'medium'

        # Documentation changes are low
        if field == 'docs':
            return 'low'

        # Name changes are medium
        if field == 'name':
            return 'medium'

        return 'low'

    async def _check_docs_changes(
        self,
        session: aiohttp.ClientSession,
        api: Dict[str, Any]
    ) -> Optional[APIChangeEvent]:
        """
        Check if API documentation has changed.

        Args:
            session: aiohttp session
            api: API data

        Returns:
            Change event if docs changed, None otherwise
        """
        if not self.config.get('change_detector.track_docs_changes', True):
            return None

        docs_url = api.get('docs', '')
        if not docs_url:
            return None

        api_id = api.get('id', 'unknown')

        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get(docs_url, timeout=timeout) as response:
                if response.status != 200:
                    return None

                content = await response.text()
                content_hash = calculate_hash(content)

                # Get previous docs hash
                previous_hash = await self.db.get_state(f'docs_hash_{api_id}')

                if previous_hash and previous_hash != content_hash:
                    # Documentation has changed
                    await self.db.set_state(f'docs_hash_{api_id}', content_hash)

                    return APIChangeEvent(
                        api_id=api_id,
                        change_type='docs_content',
                        old_value=previous_hash,
                        new_value=content_hash,
                        detected_at=timestamp_iso(),
                        severity='low',
                        metadata={'docs_url': docs_url}
                    )
                elif not previous_hash:
                    # First time checking, save hash
                    await self.db.set_state(f'docs_hash_{api_id}', content_hash)

        except Exception as e:
            self.logger.debug(f"Failed to check docs for {api_id}: {e}")

        return None

    async def run_iteration(self):
        """Execute one change detection iteration."""
        # Load directory
        await self._load_directory()

        if not self._apis:
            self.logger.warning("No APIs to check for changes")
            return

        all_changes = []

        # Check for changes in API metadata
        for api in self._apis:
            try:
                changes = await self._detect_api_changes(api)
                all_changes.extend(changes)
            except Exception as e:
                self.logger.error(f"Error detecting changes for {api.get('id')}: {e}")

        # Save all changes to database
        for change in all_changes:
            await self.db.save_change_event(change)
            self.logger.info(
                f"🔔 Change detected - API: {change.api_id}, Type: {change.change_type}, "
                f"Severity: {change.severity}, Old: {change.old_value[:50]}, "
                f"New: {change.new_value[:50]}"
            )

        # Check documentation changes (async)
        if self.config.get('change_detector.track_docs_changes', True):
            async with aiohttp.ClientSession() as session:
                docs_changes = []
                for api in self._apis[:20]:  # Limit to avoid rate limiting
                    change = await self._check_docs_changes(session, api)
                    if change:
                        docs_changes.append(change)
                        await self.db.save_change_event(change)
                    await asyncio.sleep(1)  # Rate limiting

                if docs_changes:
                    self.logger.info(f"Detected {len(docs_changes)} documentation changes")

        total_changes = len(all_changes)
        self.logger.info(f"Change detection complete: {total_changes} changes detected")

        await self.db.set_state('last_change_detection', timestamp_iso())

    def get_interval(self) -> int:
        """Get check interval from config."""
        return self.config.get('change_detector.check_interval', 1800)
