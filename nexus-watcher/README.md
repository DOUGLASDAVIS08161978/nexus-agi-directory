# 🚀 Nexus Watcher

**Autonomous daemon service that keeps the Nexus AGI Directory alive and intelligent.**

Nexus Watcher is a continuously running background service that monitors, discovers, validates, and maintains the AGI Directory autonomously. It's designed to make the directory not just a static catalog, but a living, breathing intelligence layer for AI/AGI APIs.

## 🌟 Features

### 🏥 Health Monitoring
- **Real-time health checks** for all 133+ APIs in the directory
- Concurrent endpoint testing with configurable parallelism
- Response time tracking and status code monitoring
- Failure detection with consecutive failure thresholds
- Automatic retry logic with exponential backoff

### 🔍 Discovery Scout
- **Autonomous discovery** of new AI/AGI APIs across multiple sources:
  - GitHub API search for trending AI repositories
  - Hacker News API for newly announced AI tools
  - Product Hunt integration (planned)
- **Confidence scoring** algorithm for API relevance
- Duplicate detection and intelligent filtering
- Metadata enrichment (stars, language, descriptions)

### ✅ Validator
- **Endpoint validation** for discovered APIs
- Documentation accessibility verification
- Authentication method validation
- Automatic quality assessment
- Validation queue management

### 🔔 Change Detector
- **Proactive change monitoring** for existing APIs
- Endpoint URL change detection
- API status change alerts (stable → deprecated, etc.)
- Documentation content change tracking
- Version change notifications
- Capability additions/removals tracking
- Authentication method change detection
- Severity-based change classification (low/medium/high/critical)

### 📊 Monitoring Dashboard
- **Beautiful web dashboard** with real-time stats
- REST API for programmatic access
- Health status visualization
- Discovery and change event feeds
- Worker status monitoring
- Auto-refreshing statistics

## 🏗️ Architecture

```
nexus-watcher/
├── daemon/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration manager
│   ├── engine.py            # Core daemon engine
│   ├── workers/             # Async workers
│   │   ├── base_worker.py       # Base worker class
│   │   ├── health_monitor.py   # Health checking
│   │   ├── discovery_scout.py  # API discovery
│   │   ├── validator.py        # Validation
│   │   └── change_detector.py  # Change detection
│   ├── database/            # SQLite persistence
│   │   ├── models.py           # Data models
│   │   └── db.py               # Database manager
│   ├── api/                 # FastAPI server
│   │   └── server.py           # REST API + Dashboard
│   └── utils/               # Utilities
│       ├── logger.py           # Colored logging
│       └── helpers.py          # Helper functions
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
├── run_daemon.py           # CLI runner
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

```bash
# Clone the repository
cd nexus-agi-directory/nexus-watcher

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your GitHub token (for discovery)
nano .env
```

### Configuration

Edit `config.yaml` to customize:

```yaml
daemon:
  log_level: "INFO"  # DEBUG for verbose logging

health_monitor:
  check_interval: 600  # 10 minutes
  max_concurrent: 20   # Parallel checks

discovery_scout:
  scan_interval: 3600  # 1 hour
  confidence_threshold: 0.7

api:
  port: 8080  # Dashboard port
```

### Running the Daemon

```bash
# Basic run (daemon + API dashboard)
python run_daemon.py

# With custom config
python run_daemon.py --config /path/to/config.yaml

# Daemon only (no API server)
python run_daemon.py --no-api

# Using module directly
python -m daemon.main
```

### Accessing the Dashboard

Once running, open your browser to:

```
http://localhost:8080
```

You'll see:
- 📊 Real-time daemon status
- 💚 API health statistics
- 🔍 Discovered APIs feed
- 🔔 Change detection alerts
- 👷 Worker status monitoring

## 📡 API Endpoints

### Status & Monitoring

```bash
# Daemon status
GET /api/status

# Database statistics
GET /api/stats

# Health check
GET /api/ping
```

### Health Records

```bash
# Latest health for all APIs
GET /api/health?limit=100

# Health history for specific API
GET /api/health/{api_id}?limit=50
```

### Discoveries

```bash
# Get discovered APIs
GET /api/discoveries?limit=50
```

### Changes

```bash
# Get change events
GET /api/changes?limit=100
```

### Examples

```bash
# Get daemon status
curl http://localhost:8080/api/status | jq

# Get health statistics
curl http://localhost:8080/api/stats | jq

# Get recent discoveries
curl http://localhost:8080/api/discoveries | jq

# Get change events
curl http://localhost:8080/api/changes | jq
```

## 🔧 Configuration Reference

### Daemon Settings

```yaml
daemon:
  name: "Nexus Watcher"
  version: "1.0.0"
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  state_db: "./data/nexus_watcher.db"
```

### Directory Source

```yaml
directory:
  source_file: "../.well-known/seeds-public.json"
  reload_interval: 300  # seconds
```

### Worker Settings

```yaml
health_monitor:
  enabled: true
  check_interval: 600  # seconds (10 min)
  timeout: 10
  max_concurrent: 20
  retry_attempts: 2
  failure_threshold: 3

discovery_scout:
  enabled: true
  scan_interval: 3600  # seconds (1 hour)
  sources:
    - github_api_search
    - hacker_news
  confidence_threshold: 0.7

validator:
  enabled: true
  validation_interval: 7200  # seconds (2 hours)
  check_documentation: true

change_detector:
  enabled: true
  check_interval: 1800  # seconds (30 min)
  track_docs_changes: true
```

### API Server

```yaml
api:
  enabled: true
  host: "0.0.0.0"
  port: 8080
  cors_origins: ["*"]
```

## 📊 Data Models

### Health Record
```json
{
  "api_id": "agi://service/openai/chat-completions:v1",
  "endpoint": "https://api.openai.com/v1/chat/completions",
  "status": "healthy",
  "response_time_ms": 145.2,
  "status_code": 200,
  "error_message": null,
  "checked_at": "2025-12-31T10:30:00Z",
  "consecutive_failures": 0
}
```

### Discovered API
```json
{
  "url": "https://api.example.com",
  "name": "Example AI API",
  "description": "Machine learning API",
  "source": "github",
  "confidence_score": 0.85,
  "discovered_at": "2025-12-31T10:00:00Z",
  "validated": false,
  "metadata": {
    "stars": 1250,
    "language": "Python"
  }
}
```

### Change Event
```json
{
  "api_id": "agi://service/example:v1",
  "change_type": "endpoint",
  "old_value": "https://old-api.example.com",
  "new_value": "https://new-api.example.com",
  "detected_at": "2025-12-31T09:45:00Z",
  "severity": "critical"
}
```

## 🔍 How It Works

### 1. Health Monitor Worker
- Loads all APIs from `seeds-public.json`
- Performs concurrent HTTP HEAD/GET requests
- Tracks response times and status codes
- Detects failures and marks APIs as down/degraded
- Stores results in SQLite database
- Runs every 10 minutes (configurable)

### 2. Discovery Scout Worker
- Searches GitHub API for AI-related repositories
- Scrapes Hacker News for AI tool announcements
- Calculates confidence scores based on:
  - Keyword matching (ai, ml, llm, api, etc.)
  - Repository popularity (stars)
  - Presence of homepage/docs
  - Programming language
- Filters by confidence threshold
- Stores discoveries for validation
- Runs every hour (configurable)

### 3. Validator Worker
- Processes pending discovered APIs
- Validates endpoint accessibility
- Checks documentation URLs
- Marks APIs as validated or rejected
- Updates confidence scores
- Runs every 2 hours (configurable)

### 4. Change Detector Worker
- Takes snapshots of API metadata
- Compares current state with previous snapshots
- Detects changes in:
  - Endpoints (critical)
  - API status (high)
  - Authentication methods (high)
  - Capabilities (medium)
  - Documentation (low)
  - Versions (medium)
- Assigns severity levels
- Stores change events
- Optionally monitors docs content changes
- Runs every 30 minutes (configurable)

## 🛠️ Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=daemon
```

### Code Style

```bash
# Format code
black daemon/

# Lint
flake8 daemon/

# Type checking
mypy daemon/
```

### Adding a New Worker

1. Create `daemon/workers/your_worker.py`
2. Extend `BaseWorker` class
3. Implement `run_iteration()` and `get_interval()`
4. Add to `daemon/workers/__init__.py`
5. Register in `daemon/engine.py`
6. Add config section to `config.yaml`

Example:

```python
from .base_worker import BaseWorker

class MyWorker(BaseWorker):
    def __init__(self, *args, **kwargs):
        super().__init__("my_worker", *args, **kwargs)

    async def run_iteration(self):
        # Your worker logic here
        self.logger.info("Running my worker")

    def get_interval(self) -> int:
        return self.config.get('my_worker.interval', 300)
```

## 🐛 Troubleshooting

### Daemon won't start

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Check logs
tail -f logs/nexus-watcher-*.log
```

### Health checks failing

```bash
# Increase timeout in config.yaml
health_monitor:
  timeout: 30  # Increase from 10

# Reduce concurrency
health_monitor:
  max_concurrent: 10  # Reduce from 20
```

### Discovery not working

```bash
# Check GitHub token
echo $GITHUB_TOKEN

# Verify in .env file
cat .env | grep GITHUB_TOKEN

# Check rate limits
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit
```

### Database issues

```bash
# Reset database
rm -rf data/nexus_watcher.db

# Restart daemon (will recreate schema)
python run_daemon.py
```

## 🚦 Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/nexus-watcher.service`:

```ini
[Unit]
Description=Nexus Watcher Daemon
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/nexus-agi-directory/nexus-watcher
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python run_daemon.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable nexus-watcher
sudo systemctl start nexus-watcher
sudo systemctl status nexus-watcher
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "run_daemon.py"]
```

Build and run:

```bash
docker build -t nexus-watcher .
docker run -d -p 8080:8080 \
  -e GITHUB_TOKEN=your_token \
  -v ./data:/app/data \
  nexus-watcher
```

### Using Docker Compose

```yaml
version: '3.8'

services:
  nexus-watcher:
    build: .
    ports:
      - "8080:8080"
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

## 📈 Monitoring & Alerting

### Prometheus Integration (Planned)

```yaml
# Future: Expose Prometheus metrics
GET /metrics

# Examples:
nexus_watcher_apis_total 133
nexus_watcher_apis_healthy 120
nexus_watcher_apis_down 3
nexus_watcher_discoveries_total 45
nexus_watcher_changes_detected 12
```

### Notifications (Planned)

```yaml
notifications:
  enabled: true
  slack_webhook: "https://hooks.slack.com/..."
  discord_webhook: "https://discord.com/api/webhooks/..."
  email: "alerts@nexus-agi.com"
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see parent project for details.

## 🙏 Credits

Built with ❤️ for the Nexus AGI Directory project.

**For the agents, by humans, for a world where both collaborate seamlessly.**

## 📞 Support

- Issues: [GitHub Issues](https://github.com/nexus-agi/nexus-agi-directory/issues)
- Contact: contact@nexus-agi.com
- Documentation: [Nexus AGI Directory](https://nexus-agi.com)

---

**Status:** ✨ Production Ready
**Version:** 1.0.0
**Last Updated:** 2025-12-31
