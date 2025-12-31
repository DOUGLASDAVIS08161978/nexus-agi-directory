"""Database models and schema for Nexus Watcher."""

from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class APIStatus(Enum):
    """API health status enumeration."""
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    ERROR = "error"


class DiscoverySource(Enum):
    """Sources for API discovery."""
    GITHUB = "github"
    PRODUCT_HUNT = "product_hunt"
    HACKER_NEWS = "hacker_news"
    MANUAL = "manual"
    WEB_CRAWL = "web_crawl"


@dataclass
class APIHealthRecord:
    """Health check record for an API."""
    api_id: str
    endpoint: str
    status: str
    response_time_ms: Optional[float]
    status_code: Optional[int]
    error_message: Optional[str]
    checked_at: str
    consecutive_failures: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'APIHealthRecord':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class DiscoveredAPI:
    """Discovered API candidate."""
    url: str
    name: str
    description: Optional[str]
    source: str
    confidence_score: float
    discovered_at: str
    metadata: Optional[Dict[str, Any]] = None
    validated: bool = False
    added_to_directory: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiscoveredAPI':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class APIChangeEvent:
    """API change detection event."""
    api_id: str
    change_type: str  # 'endpoint', 'docs', 'status', 'version', 'auth'
    old_value: Optional[str]
    new_value: Optional[str]
    detected_at: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'APIChangeEvent':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class DaemonState:
    """Overall daemon state."""
    last_startup: str
    total_apis_monitored: int
    total_health_checks: int
    total_discoveries: int
    total_changes_detected: int
    uptime_seconds: int
    workers_active: Dict[str, bool]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DaemonState':
        """Create from dictionary."""
        return cls(**data)


# Database schema SQL
SCHEMA_SQL = """
-- API Health Records
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    status TEXT NOT NULL,
    response_time_ms REAL,
    status_code INTEGER,
    error_message TEXT,
    checked_at TEXT NOT NULL,
    consecutive_failures INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_health_api_id ON health_records(api_id);
CREATE INDEX IF NOT EXISTS idx_health_checked_at ON health_records(checked_at);
CREATE INDEX IF NOT EXISTS idx_health_status ON health_records(status);

-- Discovered APIs
CREATE TABLE IF NOT EXISTS discovered_apis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    source TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    discovered_at TEXT NOT NULL,
    metadata TEXT,  -- JSON
    validated BOOLEAN DEFAULT 0,
    added_to_directory BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_discovered_source ON discovered_apis(source);
CREATE INDEX IF NOT EXISTS idx_discovered_validated ON discovered_apis(validated);
CREATE INDEX IF NOT EXISTS idx_discovered_added ON discovered_apis(added_to_directory);

-- Change Events
CREATE TABLE IF NOT EXISTS change_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id TEXT NOT NULL,
    change_type TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    detected_at TEXT NOT NULL,
    severity TEXT NOT NULL,
    metadata TEXT,  -- JSON
    acknowledged BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_changes_api_id ON change_events(api_id);
CREATE INDEX IF NOT EXISTS idx_changes_type ON change_events(change_type);
CREATE INDEX IF NOT EXISTS idx_changes_severity ON change_events(severity);
CREATE INDEX IF NOT EXISTS idx_changes_acknowledged ON change_events(acknowledged);

-- Daemon State
CREATE TABLE IF NOT EXISTS daemon_state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API Snapshots (for change detection)
CREATE TABLE IF NOT EXISTS api_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id TEXT NOT NULL,
    snapshot_data TEXT NOT NULL,  -- JSON
    snapshot_hash TEXT NOT NULL,
    captured_at TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_snapshots_api_id ON api_snapshots(api_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_captured_at ON api_snapshots(captured_at);
"""
