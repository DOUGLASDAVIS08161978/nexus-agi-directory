# Quick Start Guide - Nexus AGI Directory API Service

Get started with the Nexus AGI Directory API service in less than 5 minutes!

## For Users - Access the API

### 1. Get a Free API Key

```bash
curl -X POST https://nexus-agi.com/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","tier":"free"}'
```

Response:
```json
{
  "apiKey": "nxs_free_abc123...",
  "tier": "free",
  "tierDetails": {...}
}
```

### 2. Access the Directory

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  https://nexus-agi.com/api/v1/directory
```

### 3. Search for APIs

```bash
# Search by capability
curl -H "x-api-key: YOUR_API_KEY" \
  "https://nexus-agi.com/api/v1/search?capability=chat"

# Search by name
curl -H "x-api-key: YOUR_API_KEY" \
  "https://nexus-agi.com/api/v1/search?q=openai"

# Filter by status
curl -H "x-api-key: YOUR_API_KEY" \
  "https://nexus-agi.com/api/v1/search?status=stable"
```

### Demo API Keys (for testing)

```bash
# Free Tier
x-api-key: demo-free-key-12345

# Pro Tier
x-api-key: demo-pro-key-67890

# Enterprise Tier
x-api-key: demo-enterprise-key-abcdef
```

## For Developers - Run Your Own Instance

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/DOUGLASDAVIS08161978/nexus-agi-directory.git
cd nexus-agi-directory

# Build and run
docker-compose up -d

# Access at http://localhost:3000
curl http://localhost:3000/health
```

### Option 2: Node.js

```bash
# Clone the repository
git clone https://github.com/DOUGLASDAVIS08161978/nexus-agi-directory.git
cd nexus-agi-directory

# Install dependencies
npm install

# Start the service
npm start

# Access at http://localhost:3000
```

### Option 3: Cloud Deployment

**Vercel (Serverless):**
```bash
npm install -g vercel
vercel
```

**Railway (Containers):**
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

**Fly.io (Global):**
```bash
fly launch
fly deploy
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides.

## Testing Your Instance

Once your instance is running, test it:

```bash
# Health check
curl http://localhost:3000/health

# Get API info
curl http://localhost:3000/api/v1/info

# View pricing
curl http://localhost:3000/api/v1/pricing

# Register for an API key
curl -X POST http://localhost:3000/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","tier":"free"}'

# Use the API key
API_KEY="nxs_free_..."
curl -H "x-api-key: $API_KEY" http://localhost:3000/api/v1/directory
```

## Code Examples

### Python

```python
import requests

# Register
response = requests.post('https://nexus-agi.com/api/v1/register', 
    json={'email': 'your@email.com', 'tier': 'free'})
api_key = response.json()['apiKey']

# Get directory
headers = {'x-api-key': api_key}
directory = requests.get('https://nexus-agi.com/api/v1/directory', 
    headers=headers).json()

print(f"Found {directory['meta']['count']} APIs")

# Search for chat APIs
search = requests.get('https://nexus-agi.com/api/v1/search',
    headers=headers,
    params={'capability': 'chat', 'status': 'stable'}).json()

for api in search['data']:
    print(f"- {api['name']}: {api['endpoint']}")
```

### JavaScript

```javascript
// Register for API key
const registration = await fetch('https://nexus-agi.com/api/v1/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'your@email.com', tier: 'free' })
}).then(r => r.json());

const apiKey = registration.apiKey;

// Get directory
const directory = await fetch('https://nexus-agi.com/api/v1/directory', {
  headers: { 'x-api-key': apiKey }
}).then(r => r.json());

console.log(`Found ${directory.meta.count} APIs`);

// Search
const results = await fetch('https://nexus-agi.com/api/v1/search?capability=vision', {
  headers: { 'x-api-key': apiKey }
}).then(r => r.json());
```

### Go

```go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "strings"
)

func main() {
    // Register
    payload := strings.NewReader(`{"email":"your@email.com","tier":"free"}`)
    resp, _ := http.Post("https://nexus-agi.com/api/v1/register", 
        "application/json", payload)
    
    var reg map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&reg)
    apiKey := reg["apiKey"].(string)
    resp.Body.Close()

    // Get directory
    req, _ := http.NewRequest("GET", "https://nexus-agi.com/api/v1/directory", nil)
    req.Header.Set("x-api-key", apiKey)
    
    client := &http.Client{}
    resp, _ = client.Do(req)
    defer resp.Body.Close()
    
    body, _ := io.ReadAll(resp.Body)
    fmt.Println(string(body))
}
```

## Pricing

| Tier | Price | Requests/Hour | Features |
|------|-------|---------------|----------|
| **Free** | $0/mo | 60 | Directory access, basic search |
| **Pro** | $29/mo | 1,000 | Analytics, webhooks, priority support |
| **Enterprise** | $299/mo | 10,000 | Custom integration, SLA, dedicated support |

## Support

- **Documentation**: [API_DOCS.md](API_DOCS.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Email**: contact@nexus-agi.com
- **GitHub**: github.com/nexus-agi-directory/nexus-agi-directory

## What's Next?

1. **Upgrade to Pro** - Get more requests and analytics
2. **Integrate webhooks** - Get notified of directory updates
3. **Get your API listed** - Email contact@nexus-agi.com
4. **Deploy your own** - Full deployment guides available

---

**Quick Links:**
- [Full API Documentation](API_DOCS.md)
- [Deployment Guides](DEPLOYMENT.md)
- [GitHub Repository](https://github.com/DOUGLASDAVIS08161978/nexus-agi-directory)
- [Contact Support](mailto:contact@nexus-agi.com)
