"""Database manager for Nexus Watcher."""

import json
import aiosqlite
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import (
    APIHealthRecord,
    DiscoveredAPI,
    APIChangeEvent,
    DaemonState,
    SCHEMA_SQL
)
from ..utils.logger import get_logger

logger = get_logger("database")


class DatabaseManager:
    """Manages SQLite database for daemon state."""

    def __init__(self, db_path: str):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection: Optional[aiosqlite.Connection] = None

    async def connect(self):
        """Establish database connection and initialize schema."""
        self._connection = await aiosqlite.connect(str(self.db_path))
        self._connection.row_factory = aiosqlite.Row
        await self._init_schema()
        logger.info(f"Database connected: {self.db_path}")

    async def disconnect(self):
        """Close database connection."""
        if self._connection:
            await self._connection.close()
            logger.info("Database disconnected")

    async def _init_schema(self):
        """Initialize database schema."""
        async with self._connection.executescript(SCHEMA_SQL):
            await self._connection.commit()

    # Health Records
    async def save_health_record(self, record: APIHealthRecord):
        """Save API health check record."""
        query = """
        INSERT INTO health_records
        (api_id, endpoint, status, response_time_ms, status_code, error_message, checked_at, consecutive_failures)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        await self._connection.execute(
            query,
            (
                record.api_id,
                record.endpoint,
                record.status,
                record.response_time_ms,
                record.status_code,
                record.error_message,
                record.checked_at,
                record.consecutive_failures
            )
        )
        await self._connection.commit()

    async def get_latest_health(self, api_id: str) -> Optional[APIHealthRecord]:
        """Get latest health record for an API."""
        query = """
        SELECT * FROM health_records
        WHERE api_id = ?
        ORDER BY checked_at DESC
        LIMIT 1
        """
        async with self._connection.execute(query, (api_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return APIHealthRecord(**dict(row))
        return None

    async def get_health_history(self, api_id: str, limit: int = 100) -> List[APIHealthRecord]:
        """Get health history for an API."""
        query = """
        SELECT * FROM health_records
        WHERE api_id = ?
        ORDER BY checked_at DESC
        LIMIT ?
        """
        records = []
        async with self._connection.execute(query, (api_id, limit)) as cursor:
            async for row in cursor:
                records.append(APIHealthRecord(**dict(row)))
        return records

    async def get_all_latest_health(self) -> List[APIHealthRecord]:
        """Get latest health status for all APIs."""
        query = """
        SELECT * FROM health_records hr1
        WHERE checked_at = (
            SELECT MAX(checked_at)
            FROM health_records hr2
            WHERE hr2.api_id = hr1.api_id
        )
        ORDER BY api_id
        """
        records = []
        async with self._connection.execute(query) as cursor:
            async for row in cursor:
                records.append(APIHealthRecord(**dict(row)))
        return records

    # Discovered APIs
    async def save_discovered_api(self, api: DiscoveredAPI):
        """Save discovered API candidate."""
        query = """
        INSERT OR IGNORE INTO discovered_apis
        (url, name, description, source, confidence_score, discovered_at, metadata, validated, added_to_directory)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        metadata_json = json.dumps(api.metadata) if api.metadata else None
        await self._connection.execute(
            query,
            (
                api.url,
                api.name,
                api.description,
                api.source,
                api.confidence_score,
                api.discovered_at,
                metadata_json,
                api.validated,
                api.added_to_directory
            )
        )
        await self._connection.commit()

    async def get_pending_discoveries(self, limit: int = 50) -> List[DiscoveredAPI]:
        """Get discovered APIs pending validation."""
        query = """
        SELECT * FROM discovered_apis
        WHERE validated = 0
        ORDER BY confidence_score DESC, discovered_at DESC
        LIMIT ?
        """
        apis = []
        async with self._connection.execute(query, (limit,)) as cursor:
            async for row in cursor:
                data = dict(row)
                if data['metadata']:
                    data['metadata'] = json.loads(data['metadata'])
                apis.append(DiscoveredAPI(**data))
        return apis

    async def mark_discovery_validated(self, url: str, validated: bool = True):
        """Mark a discovered API as validated."""
        query = "UPDATE discovered_apis SET validated = ? WHERE url = ?"
        await self._connection.execute(query, (validated, url))
        await self._connection.commit()

    # Change Events
    async def save_change_event(self, event: APIChangeEvent):
        """Save API change event."""
        query = """
        INSERT INTO change_events
        (api_id, change_type, old_value, new_value, detected_at, severity, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        metadata_json = json.dumps(event.metadata) if event.metadata else None
        await self._connection.execute(
            query,
            (
                event.api_id,
                event.change_type,
                event.old_value,
                event.new_value,
                event.detected_at,
                event.severity,
                metadata_json
            )
        )
        await self._connection.commit()

    async def get_unacknowledged_changes(self, limit: int = 100) -> List[APIChangeEvent]:
        """Get unacknowledged change events."""
        query = """
        SELECT api_id, change_type, old_value, new_value, detected_at, severity, metadata
        FROM change_events
        WHERE acknowledged = 0
        ORDER BY severity DESC, detected_at DESC
        LIMIT ?
        """
        events = []
        async with self._connection.execute(query, (limit,)) as cursor:
            async for row in cursor:
                data = dict(row)
                if data['metadata']:
                    data['metadata'] = json.loads(data['metadata'])
                events.append(APIChangeEvent(**data))
        return events

    # State Management
    async def set_state(self, key: str, value: Any):
        """Set daemon state value."""
        query = """
        INSERT OR REPLACE INTO daemon_state (key, value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        """
        value_str = json.dumps(value) if not isinstance(value, str) else value
        await self._connection.execute(query, (key, value_str))
        await self._connection.commit()

    async def get_state(self, key: str, default: Any = None) -> Any:
        """Get daemon state value."""
        query = "SELECT value FROM daemon_state WHERE key = ?"
        async with self._connection.execute(query, (key,)) as cursor:
            row = await cursor.fetchone()
            if row:
                try:
                    return json.loads(row['value'])
                except (json.JSONDecodeError, TypeError):
                    return row['value']
        return default

    # Snapshots
    async def save_api_snapshot(self, api_id: str, snapshot_data: Dict[str, Any], snapshot_hash: str):
        """Save API snapshot for change detection."""
        query = """
        INSERT INTO api_snapshots (api_id, snapshot_data, snapshot_hash, captured_at)
        VALUES (?, ?, ?, ?)
        """
        await self._connection.execute(
            query,
            (api_id, json.dumps(snapshot_data), snapshot_hash, datetime.utcnow().isoformat())
        )
        await self._connection.commit()

    async def get_latest_snapshot(self, api_id: str) -> Optional[Dict[str, Any]]:
        """Get latest snapshot for an API."""
        query = """
        SELECT snapshot_data, snapshot_hash, captured_at
        FROM api_snapshots
        WHERE api_id = ?
        ORDER BY captured_at DESC
        LIMIT 1
        """
        async with self._connection.execute(query, (api_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    'data': json.loads(row['snapshot_data']),
                    'hash': row['snapshot_hash'],
                    'captured_at': row['captured_at']
                }
        return None

    # Statistics
    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {}

        # Total health checks
        async with self._connection.execute("SELECT COUNT(*) as count FROM health_records") as cursor:
            row = await cursor.fetchone()
            stats['total_health_checks'] = row['count']

        # Total discoveries
        async with self._connection.execute("SELECT COUNT(*) as count FROM discovered_apis") as cursor:
            row = await cursor.fetchone()
            stats['total_discoveries'] = row['count']

        # Pending validations
        async with self._connection.execute(
            "SELECT COUNT(*) as count FROM discovered_apis WHERE validated = 0"
        ) as cursor:
            row = await cursor.fetchone()
            stats['pending_validations'] = row['count']

        # Total changes
        async with self._connection.execute("SELECT COUNT(*) as count FROM change_events") as cursor:
            row = await cursor.fetchone()
            stats['total_changes'] = row['count']

        # Unacknowledged changes
        async with self._connection.execute(
            "SELECT COUNT(*) as count FROM change_events WHERE acknowledged = 0"
        ) as cursor:
            row = await cursor.fetchone()
            stats['unacknowledged_changes'] = row['count']

        # APIs by status
        async with self._connection.execute("""
            SELECT status, COUNT(*) as count
            FROM (
                SELECT DISTINCT api_id,
                    FIRST_VALUE(status) OVER (PARTITION BY api_id ORDER BY checked_at DESC) as status
                FROM health_records
            )
            GROUP BY status
        """) as cursor:
            status_counts = {}
            async for row in cursor:
                status_counts[row['status']] = row['count']
            stats['apis_by_status'] = status_counts

        return stats
