"""Main entry point for Nexus Watcher daemon."""

import asyncio
import sys
from pathlib import Path

from .engine import NexusWatcherEngine
from .api.server import run_api_server
from .utils.logger import get_logger


async def run_daemon_with_api(config_path: str = None):
    """
    Run daemon with API server.

    Args:
        config_path: Path to config file
    """
    engine = NexusWatcherEngine(config_path)
    logger = get_logger("main")

    # Initialize engine
    await engine.initialize()

    # Start daemon
    await engine.start()

    # Start API server if enabled
    if engine.config.get('api.enabled', True):
        logger.info("Starting API server...")
        api_task = asyncio.create_task(run_api_server(engine))

        try:
            # Keep running
            while engine._running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        finally:
            await engine.stop()
            api_task.cancel()
            try:
                await api_task
            except asyncio.CancelledError:
                pass
    else:
        # Run daemon without API
        await engine.run_forever()


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Nexus Watcher - Autonomous daemon for AGI Directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run daemon with default config
  python -m daemon.main

  # Run with custom config
  python -m daemon.main --config /path/to/config.yaml

  # Run daemon without API server
  python -m daemon.main --no-api

For more information, visit: https://github.com/nexus-agi/nexus-agi-directory
        """
    )

    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to configuration file (default: config.yaml)'
    )

    parser.add_argument(
        '--no-api',
        action='store_true',
        help='Run daemon without API server'
    )

    args = parser.parse_args()

    # Disable API if requested
    if args.no_api:
        from .config import Config
        config = Config(args.config)
        config.set('api.enabled', False)

    try:
        asyncio.run(run_daemon_with_api(args.config))
    except KeyboardInterrupt:
        print("\n👋 Nexus Watcher stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
