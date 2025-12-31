"""Core daemon engine for Nexus Watcher."""

import asyncio
import signal
from typing import List, Optional
from datetime import datetime

from .config import Config
from .database.db import DatabaseManager
from .workers import (
    HealthMonitorWorker,
    DiscoveryScoutWorker,
    ValidatorWorker,
    ChangeDetectorWorker
)
from .utils.logger import DaemonLogger, get_logger


class NexusWatcherEngine:
    """Main daemon engine that orchestrates all workers."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the daemon engine.

        Args:
            config_path: Path to config file (optional)
        """
        self.config = Config(config_path)
        self.logger = DaemonLogger.setup(
            level=self.config.get('daemon.log_level', 'INFO'),
            log_dir='./logs'
        )

        self.db: Optional[DatabaseManager] = None
        self.workers: List = []
        self._running = False
        self._start_time: Optional[datetime] = None

    async def initialize(self):
        """Initialize database and workers."""
        self.logger.info("Initializing Nexus Watcher daemon...")

        # Initialize database
        db_path = self.config.get('daemon.state_db', './data/nexus_watcher.db')
        self.db = DatabaseManager(db_path)
        await self.db.connect()

        # Initialize workers
        self.workers = [
            HealthMonitorWorker(self.config, self.db),
            DiscoveryScoutWorker(self.config, self.db),
            ValidatorWorker(self.config, self.db),
            ChangeDetectorWorker(self.config, self.db)
        ]

        # Save initialization state
        await self.db.set_state('daemon_version', '1.0.0')
        await self.db.set_state('last_startup', datetime.utcnow().isoformat())

        self.logger.info(f"Initialized {len(self.workers)} workers")

    async def start(self):
        """Start the daemon and all workers."""
        if self._running:
            self.logger.warning("Daemon already running")
            return

        self._running = True
        self._start_time = datetime.utcnow()

        self.logger.info("=" * 60)
        self.logger.info("🚀 Starting Nexus Watcher Daemon")
        self.logger.info("=" * 60)

        # Start all workers
        for worker in self.workers:
            try:
                await worker.start()
            except Exception as e:
                self.logger.error(f"Failed to start worker {worker.name}: {e}")

        # Log active workers
        active_workers = [w.name for w in self.workers if w._running]
        self.logger.info(f"Active workers: {', '.join(active_workers)}")

        # Set up signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))

        self.logger.info("Daemon is now running. Press Ctrl+C to stop.")

    async def stop(self):
        """Stop the daemon and all workers."""
        if not self._running:
            return

        self.logger.info("Stopping Nexus Watcher daemon...")
        self._running = False

        # Stop all workers
        stop_tasks = [worker.stop() for worker in self.workers]
        await asyncio.gather(*stop_tasks, return_exceptions=True)

        # Close database
        if self.db:
            await self.db.disconnect()

        uptime = (datetime.utcnow() - self._start_time).total_seconds() if self._start_time else 0
        self.logger.info(f"Daemon stopped (uptime: {uptime:.0f}s)")

    async def run_forever(self):
        """Run the daemon indefinitely."""
        await self.initialize()
        await self.start()

        try:
            # Keep the daemon running
            while self._running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt")
        finally:
            await self.stop()

    def get_status(self) -> dict:
        """
        Get daemon status.

        Returns:
            Status dictionary
        """
        uptime = None
        if self._start_time:
            uptime = (datetime.utcnow() - self._start_time).total_seconds()

        workers_status = [worker.get_status() for worker in self.workers]

        return {
            'daemon': {
                'name': self.config.get('daemon.name', 'Nexus Watcher'),
                'version': self.config.get('daemon.version', '1.0.0'),
                'running': self._running,
                'uptime_seconds': uptime,
                'start_time': self._start_time.isoformat() if self._start_time else None,
            },
            'workers': workers_status
        }
