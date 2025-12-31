"""Validator worker for endpoint verification."""

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

from .base_worker import BaseWorker
from ..database.models import DiscoveredAPI
from ..utils.helpers import timestamp_iso, validate_url


class ValidatorWorker(BaseWorker):
    """Worker that validates discovered APIs and endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__("validator", *args, **kwargs)

    async def _validate_endpoint(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> Dict[str, Any]:
        """
        Validate an endpoint.

        Args:
            session: aiohttp session
            url: Endpoint URL to validate

        Returns:
            Validation result dictionary
        """
        result = {
            'url': url,
            'valid': False,
            'accessible': False,
            'status_code': None,
            'response_time_ms': None,
            'content_type': None,
            'error': None
        }

        if not validate_url(url):
            result['error'] = 'Invalid URL format'
            return result

        try:
            timeout = aiohttp.ClientTimeout(total=10)
            start_time = asyncio.get_event_loop().time()

            async with session.get(url, timeout=timeout, allow_redirects=True) as response:
                response_time = (asyncio.get_event_loop().time() - start_time) * 1000

                result['accessible'] = True
                result['status_code'] = response.status
                result['response_time_ms'] = response_time
                result['content_type'] = response.headers.get('Content-Type', '')

                # Consider successful if 2xx or 3xx
                if 200 <= response.status < 400:
                    result['valid'] = True
                else:
                    result['error'] = f'HTTP {response.status}'

        except asyncio.TimeoutError:
            result['error'] = 'Timeout'
        except aiohttp.ClientError as e:
            result['error'] = f'Client error: {str(e)}'
        except Exception as e:
            result['error'] = f'Error: {str(e)}'

        return result

    async def _check_documentation(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> bool:
        """
        Check if documentation URL is accessible.

        Args:
            session: aiohttp session
            url: Documentation URL

        Returns:
            True if accessible, False otherwise
        """
        if not validate_url(url):
            return False

        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.head(url, timeout=timeout, allow_redirects=True) as response:
                return 200 <= response.status < 400
        except Exception:
            return False

    async def _validate_api(
        self,
        session: aiohttp.ClientSession,
        api_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate an API from the directory.

        Args:
            session: aiohttp session
            api_data: API data dictionary

        Returns:
            Validation report
        """
        api_id = api_data.get('id', 'unknown')
        endpoint = api_data.get('endpoint', '')
        docs_url = api_data.get('docs', '')

        report = {
            'api_id': api_id,
            'endpoint_validation': None,
            'docs_accessible': None,
            'overall_valid': False,
            'issues': []
        }

        # Validate endpoint
        if endpoint:
            endpoint_result = await self._validate_endpoint(session, endpoint)
            report['endpoint_validation'] = endpoint_result

            if not endpoint_result['valid']:
                report['issues'].append(f"Endpoint validation failed: {endpoint_result.get('error', 'Unknown')}")
        else:
            report['issues'].append("No endpoint defined")

        # Check documentation
        if self.config.get('validator.check_documentation', True):
            if docs_url:
                docs_accessible = await self._check_documentation(session, docs_url)
                report['docs_accessible'] = docs_accessible

                if not docs_accessible:
                    report['issues'].append("Documentation URL not accessible")
            else:
                report['issues'].append("No documentation URL provided")

        # Overall validation
        endpoint_valid = report['endpoint_validation'] and report['endpoint_validation']['valid']
        docs_ok = not self.config.get('validator.check_documentation', True) or report['docs_accessible']

        report['overall_valid'] = endpoint_valid and docs_ok and len(report['issues']) == 0

        return report

    async def _validate_discovered_apis(self, session: aiohttp.ClientSession):
        """Validate pending discovered APIs."""
        pending = await self.db.get_pending_discoveries(limit=50)

        if not pending:
            self.logger.debug("No pending discoveries to validate")
            return

        self.logger.info(f"Validating {len(pending)} discovered APIs")

        validated = 0
        rejected = 0

        for api in pending:
            try:
                result = await self._validate_endpoint(session, api.url)

                # Mark as validated if endpoint is accessible
                if result['valid']:
                    await self.db.mark_discovery_validated(api.url, True)
                    validated += 1
                    self.logger.info(
                        f"✓ Validated discovered API: {api.name} ({api.url}) - "
                        f"Score: {api.confidence_score:.2f}, Source: {api.source}"
                    )
                else:
                    # Mark as validated but with negative result
                    await self.db.mark_discovery_validated(api.url, False)
                    rejected += 1
                    self.logger.debug(
                        f"✗ Rejected discovered API: {api.name} - {result.get('error', 'Invalid')}"
                    )

                # Rate limiting
                await asyncio.sleep(0.5)

            except Exception as e:
                self.logger.error(f"Validation error for {api.url}: {e}")

        self.logger.info(f"Validation complete: {validated} validated, {rejected} rejected")

    async def run_iteration(self):
        """Execute one validation iteration."""
        async with aiohttp.ClientSession() as session:
            # Validate discovered APIs
            await self._validate_discovered_apis(session)

            # Could also re-validate existing directory entries here
            # For now, health monitoring handles that

        await self.db.set_state('last_validation_run', timestamp_iso())

    def get_interval(self) -> int:
        """Get validation interval from config."""
        return self.config.get('validator.validation_interval', 7200)
