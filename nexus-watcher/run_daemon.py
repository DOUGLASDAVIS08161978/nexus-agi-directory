#!/usr/bin/env python3
"""
Nexus Watcher Daemon Runner

Simple CLI runner for the Nexus Watcher daemon service.
"""

import sys
from pathlib import Path

# Add daemon directory to path
sys.path.insert(0, str(Path(__file__).parent))

from daemon.main import main

if __name__ == '__main__':
    main()
