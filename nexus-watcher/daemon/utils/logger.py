"""Logging configuration for Nexus Watcher daemon."""

import logging
import sys
from pathlib import Path
from datetime import datetime
import colorlog


class DaemonLogger:
    """Custom logger for the daemon with color support."""

    @staticmethod
    def setup(name: str = "nexus-watcher", level: str = "INFO", log_dir: str = None):
        """
        Set up logging with color support.

        Args:
            name: Logger name
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir: Directory for log files (optional)

        Returns:
            Logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))

        # Remove existing handlers
        logger.handlers.clear()

        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))

        color_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(color_formatter)
        logger.addHandler(console_handler)

        # File handler (if log_dir specified)
        if log_dir:
            log_path = Path(log_dir)
            log_path.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d')
            file_handler = logging.FileHandler(
                log_path / f"nexus-watcher-{timestamp}.log"
            )
            file_handler.setLevel(logging.DEBUG)  # Always log everything to file

            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (defaults to root nexus-watcher logger)

    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"nexus-watcher.{name}")
    return logging.getLogger("nexus-watcher")
