"""FastAPI server for monitoring and control."""

import asyncio
from typing import Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from ..engine import NexusWatcherEngine
from ..database.db import DatabaseManager
from ..utils.logger import get_logger

logger = get_logger("api")


# Pydantic models for API responses
class DaemonStatus(BaseModel):
    """Daemon status response model."""
    name: str
    version: str
    running: bool
    uptime_seconds: Optional[float]
    start_time: Optional[str]


class WorkerStatus(BaseModel):
    """Worker status response model."""
    name: str
    running: bool
    enabled: bool
    interval: int
    uptime_seconds: Optional[float]
    start_time: Optional[str]


class HealthRecordResponse(BaseModel):
    """Health record response model."""
    api_id: str
    endpoint: str
    status: str
    response_time_ms: Optional[float]
    status_code: Optional[int]
    error_message: Optional[str]
    checked_at: str
    consecutive_failures: int


class DiscoveredAPIResponse(BaseModel):
    """Discovered API response model."""
    url: str
    name: str
    description: Optional[str]
    source: str
    confidence_score: float
    discovered_at: str
    validated: bool
    added_to_directory: bool


class ChangeEventResponse(BaseModel):
    """Change event response model."""
    api_id: str
    change_type: str
    old_value: Optional[str]
    new_value: Optional[str]
    detected_at: str
    severity: str


class StatsResponse(BaseModel):
    """Statistics response model."""
    total_health_checks: int
    total_discoveries: int
    pending_validations: int
    total_changes: int
    unacknowledged_changes: int
    apis_by_status: dict


def create_app(engine: NexusWatcherEngine) -> FastAPI:
    """
    Create FastAPI application.

    Args:
        engine: Daemon engine instance

    Returns:
        FastAPI app
    """
    app = FastAPI(
        title="Nexus Watcher API",
        description="Monitoring and control API for Nexus Watcher daemon",
        version="1.0.0"
    )

    # CORS middleware
    cors_origins = engine.config.get('api.cors_origins', ['*'])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Root endpoint - Dashboard HTML
    @app.get("/", response_class=HTMLResponse)
    async def dashboard():
        """Serve dashboard HTML."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Nexus Watcher Dashboard</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                    padding: 20px;
                }
                .container { max-width: 1200px; margin: 0 auto; }
                .header {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    margin-bottom: 20px;
                }
                .header h1 { color: #667eea; margin-bottom: 10px; }
                .header p { color: #666; }
                .cards {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-bottom: 20px;
                }
                .card {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }
                .card h2 {
                    font-size: 18px;
                    color: #667eea;
                    margin-bottom: 15px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                }
                .stat { margin: 10px 0; }
                .stat-label { color: #666; font-size: 14px; }
                .stat-value {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-top: 5px;
                }
                .status-badge {
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                    text-transform: uppercase;
                }
                .status-running { background: #10b981; color: white; }
                .status-stopped { background: #ef4444; color: white; }
                .status-healthy { background: #10b981; color: white; }
                .status-down { background: #ef4444; color: white; }
                .status-degraded { background: #f59e0b; color: white; }
                .api-links {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }
                .api-links h2 { color: #667eea; margin-bottom: 15px; }
                .api-links a {
                    display: block;
                    color: #667eea;
                    text-decoration: none;
                    padding: 10px;
                    margin: 5px 0;
                    border-radius: 5px;
                    transition: background 0.3s;
                }
                .api-links a:hover { background: #f3f4f6; }
                .footer {
                    text-align: center;
                    color: white;
                    margin-top: 30px;
                    opacity: 0.8;
                }
            </style>
            <script>
                async function loadStatus() {
                    try {
                        const response = await fetch('/api/status');
                        const data = await response.json();

                        // Update daemon status
                        document.getElementById('daemon-status').innerHTML =
                            data.daemon.running ?
                            '<span class="status-badge status-running">Running</span>' :
                            '<span class="status-badge status-stopped">Stopped</span>';

                        document.getElementById('daemon-uptime').textContent =
                            data.daemon.uptime_seconds ?
                            Math.floor(data.daemon.uptime_seconds / 60) + ' minutes' :
                            'N/A';

                        // Update workers
                        const workersDiv = document.getElementById('workers-list');
                        workersDiv.innerHTML = data.workers.map(w => `
                            <div class="stat">
                                <span class="stat-label">${w.name}:</span>
                                ${w.running ?
                                '<span class="status-badge status-running">Active</span>' :
                                '<span class="status-badge status-stopped">Inactive</span>'}
                            </div>
                        `).join('');

                        // Load stats
                        const statsResponse = await fetch('/api/stats');
                        const stats = await statsResponse.json();

                        document.getElementById('total-checks').textContent = stats.total_health_checks;
                        document.getElementById('total-discoveries').textContent = stats.total_discoveries;
                        document.getElementById('total-changes').textContent = stats.total_changes;
                        document.getElementById('pending-validations').textContent = stats.pending_validations;

                    } catch (error) {
                        console.error('Failed to load status:', error);
                    }
                }

                // Load status on page load and refresh every 10 seconds
                loadStatus();
                setInterval(loadStatus, 10000);
            </script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Nexus Watcher Dashboard</h1>
                    <p>Autonomous daemon service keeping the AGI Directory alive and intelligent</p>
                </div>

                <div class="cards">
                    <div class="card">
                        <h2>Daemon Status</h2>
                        <div class="stat">
                            <div class="stat-label">Status</div>
                            <div class="stat-value" id="daemon-status">Loading...</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Uptime</div>
                            <div class="stat-value" id="daemon-uptime">Loading...</div>
                        </div>
                    </div>

                    <div class="card">
                        <h2>Statistics</h2>
                        <div class="stat">
                            <div class="stat-label">Health Checks</div>
                            <div class="stat-value" id="total-checks">-</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">APIs Discovered</div>
                            <div class="stat-value" id="total-discoveries">-</div>
                        </div>
                    </div>

                    <div class="card">
                        <h2>Activity</h2>
                        <div class="stat">
                            <div class="stat-label">Changes Detected</div>
                            <div class="stat-value" id="total-changes">-</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">Pending Validations</div>
                            <div class="stat-value" id="pending-validations">-</div>
                        </div>
                    </div>
                </div>

                <div class="cards">
                    <div class="card">
                        <h2>Active Workers</h2>
                        <div id="workers-list">Loading...</div>
                    </div>

                    <div class="card api-links">
                        <h2>API Endpoints</h2>
                        <a href="/api/status" target="_blank">📊 /api/status - Daemon status</a>
                        <a href="/api/stats" target="_blank">📈 /api/stats - Statistics</a>
                        <a href="/api/health" target="_blank">💚 /api/health - Health records</a>
                        <a href="/api/discoveries" target="_blank">🔍 /api/discoveries - Discovered APIs</a>
                        <a href="/api/changes" target="_blank">🔔 /api/changes - Change events</a>
                        <a href="/docs" target="_blank">📚 /docs - API Documentation</a>
                    </div>
                </div>

                <div class="footer">
                    <p>Nexus Watcher v1.0.0 | For the agents, by humans</p>
                </div>
            </div>
        </body>
        </html>
        """

    # API Endpoints
    @app.get("/api/status")
    async def get_status():
        """Get daemon and worker status."""
        return engine.get_status()

    @app.get("/api/stats", response_model=StatsResponse)
    async def get_stats():
        """Get database statistics."""
        if not engine.db:
            raise HTTPException(status_code=503, detail="Database not initialized")
        return await engine.db.get_stats()

    @app.get("/api/health", response_model=List[HealthRecordResponse])
    async def get_health_records(limit: int = 100):
        """Get latest health records for all APIs."""
        if not engine.db:
            raise HTTPException(status_code=503, detail="Database not initialized")

        records = await engine.db.get_all_latest_health()
        return [r.to_dict() for r in records[:limit]]

    @app.get("/api/health/{api_id}", response_model=List[HealthRecordResponse])
    async def get_api_health_history(api_id: str, limit: int = 100):
        """Get health history for a specific API."""
        if not engine.db:
            raise HTTPException(status_code=503, detail="Database not initialized")

        records = await engine.db.get_health_history(api_id, limit)
        return [r.to_dict() for r in records]

    @app.get("/api/discoveries", response_model=List[DiscoveredAPIResponse])
    async def get_discoveries(limit: int = 50):
        """Get discovered APIs."""
        if not engine.db:
            raise HTTPException(status_code=503, detail="Database not initialized")

        discoveries = await engine.db.get_pending_discoveries(limit)
        return [d.to_dict() for d in discoveries]

    @app.get("/api/changes", response_model=List[ChangeEventResponse])
    async def get_changes(limit: int = 100):
        """Get recent change events."""
        if not engine.db:
            raise HTTPException(status_code=503, detail="Database not initialized")

        changes = await engine.db.get_unacknowledged_changes(limit)
        return [c.to_dict() for c in changes]

    @app.get("/api/ping")
    async def ping():
        """Health check endpoint."""
        return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

    return app


async def run_api_server(engine: NexusWatcherEngine):
    """
    Run the FastAPI server.

    Args:
        engine: Daemon engine instance
    """
    import uvicorn

    host = engine.config.get('api.host', '0.0.0.0')
    port = engine.config.get('api.port', 8080)

    logger.info(f"Starting API server on http://{host}:{port}")

    app = create_app(engine)

    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_level="info"
    )

    server = uvicorn.Server(config)
    await server.serve()
