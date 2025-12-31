"""Base worker class for Nexus Watcher daemon."""

import asyncio
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from ..utils.logger import get_logger
from ..database.db import DatabaseManager
from ..config import Config


class BaseWorker(ABC):
    """Abstract base class for daemon workers."""

    def __init__(self, name: str, config: Config, db: DatabaseManager):
        """
        Initialize worker.

        Args:
            name: Worker name
            config: Configuration manager
            db: Database manager
        """
        self.name = name
        self.config = config
        self.db = db
        self.logger = get_logger(f"worker.{name}")
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._start_time: Optional[datetime] = None

    @abstractmethod
    async def run_iteration(self):
        """
        Execute one iteration of the worker's task.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_interval(self) -> int:
        """
        Get the interval (in seconds) between iterations.
        Must be implemented by subclasses.

        Returns:
            Interval in seconds
        """
        pass

    def is_enabled(self) -> bool:
        """
        Check if worker is enabled in configuration.

        Returns:
            True if enabled, False otherwise
        """
        return self.config.get(f"{self.name}.enabled", True)

    async def start(self):
        """Start the worker."""
        if self._running:
            self.logger.warning(f"{self.name} already running")
            return

        if not self.is_enabled():
            self.logger.info(f"{self.name} is disabled in config")
            return

        self._running = True
        self._start_time = datetime.utcnow()
        self._task = asyncio.create_task(self._run_loop())
        self.logger.info(f"{self.name} started")

    async def stop(self):
        """Stop the worker."""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        self.logger.info(f"{self.name} stopped")

    async def _run_loop(self):
        """Main worker loop."""
        interval = self.get_interval()
        self.logger.info(f"{self.name} loop started (interval: {interval}s)")

        while self._running:
            try:
                iteration_start = datetime.utcnow()
                self.logger.debug(f"{self.name} iteration starting")

                # Run the worker's main task
                await self.run_iteration()

                # Calculate how long the iteration took
                iteration_time = (datetime.utcnow() - iteration_start).total_seconds()
                self.logger.debug(
                    f"{self.name} iteration completed in {iteration_time:.2f}s"
                )

                # Sleep for remaining interval time
                sleep_time = max(0, interval - iteration_time)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

            except asyncio.CancelledError:
                self.logger.info(f"{self.name} loop cancelled")
                break
            except Exception as e:
                self.logger.error(f"{self.name} iteration error: {e}", exc_info=True)
                # Sleep on error to prevent tight error loops
                await asyncio.sleep(min(interval, 60))

    def get_status(self) -> dict:
        """
        Get worker status information.

        Returns:
            Status dictionary
        """
        uptime = None
        if self._start_time:
            uptime = (datetime.utcnow() - self._start_time).total_seconds()

        return {
            'name': self.name,
            'running': self._running,
            'enabled': self.is_enabled(),
            'interval': self.get_interval(),
            'uptime_seconds': uptime,
            'start_time': self._start_time.isoformat() if self._start_time else None,
        }
