# Nexus AGI Directory API Documentation

## Overview

The Nexus AGI Directory API provides machine-readable access to a curated directory of 133+ AI/AGI APIs. The service is designed for autonomous agents and developers building AI-powered applications.

## Base URL

- Production: `https://nexus-agi.com`
- Local Development: `http://localhost:3000`

## Authentication

Include your API key in requests using either:
- **Header**: `x-api-key: YOUR_API_KEY`
- **Query Parameter**: `?api_key=YOUR_API_KEY`

### Getting an API Key

**Free Tier** (No credit card required):
```bash
curl -X POST https://nexus-agi.com/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email": "your@email.com", "tier": "free"}'
```

## Pricing Tiers

### Free Tier - $0/month
- ✅ 60 requests/hour
- ✅ Access to public API directory
- ✅ Basic search functionality
- ❌ No analytics
- ❌ No webhooks

### Pro Tier - $29/month
- ✅ 1,000 requests/hour
- ✅ Access to public API directory
- ✅ Advanced search with filters
- ✅ Usage analytics dashboard
- ✅ Priority support
- ✅ Webhook notifications
- ✅ API key management

### Enterprise Tier - $299/month
- ✅ 10,000 requests/hour
- ✅ Everything in Pro
- ✅ Custom API integrations
- ✅ SLA guarantee (99.9% uptime)
- ✅ Dedicated support
- ✅ Custom rate limits available
- ✅ Early access to new features

Contact: contact@nexus-agi.com for Enterprise

## Endpoints

### 1. Health Check

Check service status.

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-29T23:00:00.000Z",
  "service": "nexus-agi-directory"
}
```

### 2. API Information

Get service information and available endpoints.

```bash
GET /api/v1/info
```

**Response:**
```json
{
  "name": "Nexus AGI Directory API",
  "version": "1.0.0",
  "description": "Machine-readable API discovery for autonomous agents",
  "endpoints": {
    "directory": "/api/v1/directory",
    "search": "/api/v1/search",
    "pricing": "/api/v1/pricing",
    "register": "/api/v1/register"
  },
  "authentication": "API Key (x-api-key header or api_key query parameter)",
  "documentation": "https://nexus-agi.com/docs"
}
```

### 3. Get Pricing

View available pricing tiers.

```bash
GET /api/v1/pricing
```

**Response:**
```json
{
  "tiers": [
    {
      "id": "free",
      "name": "Free",
      "rateLimit": 60,
      "features": ["basic_directory", "public_apis"],
      "price": 0
    },
    {
      "id": "pro",
      "name": "Pro",
      "rateLimit": 1000,
      "features": ["basic_directory", "public_apis", "analytics", "priority_support", "webhooks"],
      "price": 29
    },
    {
      "id": "enterprise",
      "name": "Enterprise",
      "rateLimit": 10000,
      "features": ["basic_directory", "public_apis", "analytics", "priority_support", "webhooks", "custom_integration", "sla"],
      "price": 299
    }
  ],
  "contact": "contact@nexus-agi.com"
}
```

### 4. Get Full Directory

Retrieve the complete API directory.

**Authentication:** Optional (required for higher rate limits)

```bash
# Without authentication (free tier limits)
curl https://nexus-agi.com/api/v1/directory

# With authentication
curl -H "x-api-key: YOUR_API_KEY" \
  https://nexus-agi.com/api/v1/directory
```

**Response:**
```json
{
  "meta": {
    "tier": "pro",
    "authenticated": true,
    "count": 133,
    "timestamp": "2025-12-29T23:00:00.000Z",
    "rateLimit": {
      "limit": 1000,
      "remaining": 999
    }
  },
  "data": [
    {
      "id": "agi://service/openai/chat-completions:v1",
      "name": "OpenAI Chat Completions",
      "endpoint": "https://api.openai.com/v1/chat/completions",
      "capabilities": ["chat", "stream", "function_calling"],
      "auth": {
        "method": "bearer",
        "header": "Authorization: Bearer ${OPENAI_API_KEY}"
      },
      "docs": "https://platform.openai.com/docs/api-reference/chat",
      "status": "stable"
    }
    // ... 132 more APIs
  ]
}
```

### 5. Search APIs

Search for specific APIs by name, capability, or status.

**Authentication:** Required

**Query Parameters:**
- `q` - Search query (searches name, id, and notes)
- `capability` - Filter by capability (e.g., "chat", "vision", "tools")
- `status` - Filter by status ("stable", "beta", "experimental", "deprecated")

```bash
# Search by name
curl -H "x-api-key: YOUR_API_KEY" \
  "https://nexus-agi.com/api/v1/search?q=openai"

# Filter by capability
curl -H "x-api-key: YOUR_API_KEY" \
  "https://nexus-agi.com/api/v1/search?capability=vision"

# Filter by status
curl -H "x-api-key: YOUR_API_KEY" \
  "https://nexus-agi.com/api/v1/search?status=stable"

# Combine filters
curl -H "x-api-key: YOUR_API_KEY" \
  "https://nexus-agi.com/api/v1/search?capability=chat&status=stable"
```

**Response:**
```json
{
  "meta": {
    "tier": "pro",
    "query": {
      "q": "openai",
      "capability": null,
      "status": null
    },
    "count": 5,
    "timestamp": "2025-12-29T23:00:00.000Z"
  },
  "data": [
    {
      "id": "agi://service/openai/chat-completions:v1",
      "name": "OpenAI Chat Completions",
      "endpoint": "https://api.openai.com/v1/chat/completions",
      "capabilities": ["chat", "stream", "function_calling"],
      "status": "stable"
    }
    // ... more results
  ]
}
```

**Result Limits by Tier:**
- Free: 10 results
- Pro: 50 results
- Enterprise: Unlimited

### 6. Register API Key

Create a new API key.

```bash
POST /api/v1/register
Content-Type: application/json

{
  "email": "your@email.com",
  "tier": "free"
}
```

**Response:**
```json
{
  "message": "API key created successfully",
  "apiKey": "nxs_free_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "tier": "free",
  "tierDetails": {
    "name": "Free",
    "rateLimit": 60,
    "features": ["basic_directory", "public_apis"],
    "price": 0
  },
  "usage": "Include this key in x-api-key header or api_key query parameter",
  "example": "curl -H \"x-api-key: nxs_free_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6\" https://nexus-agi.com/api/v1/directory"
}
```

### 7. Usage Analytics

View your API usage statistics (Pro and Enterprise only).

**Authentication:** Required

```bash
curl -H "x-api-key: YOUR_API_KEY" \
  https://nexus-agi.com/api/v1/analytics
```

**Response:**
```json
{
  "apiKey": "nxs_pro_a1b2c3d4e5f6...",
  "tier": "pro",
  "usage": 342,
  "createdAt": "2025-12-01T00:00:00.000Z",
  "rateLimit": 1000,
  "features": ["basic_directory", "public_apis", "analytics", "priority_support", "webhooks"]
}
```

### 8. Legacy Endpoint

Direct access to seeds-public.json (backward compatibility).

```bash
GET /.well-known/seeds-public.json
```

Returns raw JSON array without metadata or rate limiting.

## Rate Limiting

Rate limits are enforced per API key per hour:

- **Free Tier**: 60 requests/hour
- **Pro Tier**: 1,000 requests/hour
- **Enterprise Tier**: 10,000 requests/hour

### Rate Limit Headers

```
RateLimit-Limit: 1000
RateLimit-Remaining: 999
RateLimit-Reset: 1672358400
```

### Rate Limit Exceeded Response

```json
{
  "error": "Rate limit exceeded",
  "tier": "free",
  "limit": 60,
  "upgrade": "Consider upgrading to Pro for higher limits"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Please provide at least one search parameter: q, capability, or status"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid API key"
}
```

### 403 Forbidden
```json
{
  "error": "Analytics not available on free tier",
  "upgrade": "Upgrade to Pro for analytics access"
}
```

### 404 Not Found
```json
{
  "error": "Not found",
  "message": "See /api/v1/info for available endpoints"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "tier": "free",
  "limit": 60,
  "upgrade": "Consider upgrading to Pro for higher limits"
}
```

### 500 Internal Server Error
```json
{
  "error": "Failed to load directory"
}
```

## Code Examples

### Python

```python
import requests

# Register for an API key
response = requests.post('https://nexus-agi.com/api/v1/register', 
    json={'email': 'your@email.com', 'tier': 'free'})
api_key = response.json()['apiKey']

# Get full directory
headers = {'x-api-key': api_key}
directory = requests.get('https://nexus-agi.com/api/v1/directory', 
    headers=headers).json()

print(f"Found {directory['meta']['count']} APIs")

# Search for chat APIs
chat_apis = requests.get('https://nexus-agi.com/api/v1/search',
    headers=headers,
    params={'capability': 'chat', 'status': 'stable'}).json()

# Use an API from the directory
openai_api = chat_apis['data'][0]
print(f"Using {openai_api['name']}")
print(f"Endpoint: {openai_api['endpoint']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_BASE = 'https://nexus-agi.com';

async function main() {
  // Register for API key
  const { data: registration } = await axios.post(`${API_BASE}/api/v1/register`, {
    email: 'your@email.com',
    tier: 'free'
  });
  
  const apiKey = registration.apiKey;
  const headers = { 'x-api-key': apiKey };
  
  // Get directory
  const { data: directory } = await axios.get(`${API_BASE}/api/v1/directory`, { headers });
  console.log(`Found ${directory.meta.count} APIs`);
  
  // Search for vision-capable APIs
  const { data: results } = await axios.get(`${API_BASE}/api/v1/search`, {
    headers,
    params: { capability: 'vision' }
  });
  
  console.log(`Found ${results.meta.count} vision APIs`);
}

main();
```

### cURL

```bash
# Get API key
API_KEY=$(curl -X POST https://nexus-agi.com/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","tier":"free"}' | jq -r '.apiKey')

# Get directory
curl -H "x-api-key: $API_KEY" \
  https://nexus-agi.com/api/v1/directory | jq '.meta'

# Search for stable APIs
curl -H "x-api-key: $API_KEY" \
  "https://nexus-agi.com/api/v1/search?status=stable" | jq '.data[].name'
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

const apiBase = "https://nexus-agi.com"

func main() {
    // Register for API key
    payload := strings.NewReader(`{"email":"your@email.com","tier":"free"}`)
    resp, _ := http.Post(apiBase+"/api/v1/register", "application/json", payload)
    defer resp.Body.Close()
    
    var registration map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&registration)
    apiKey := registration["apiKey"].(string)
    
    // Get directory
    req, _ := http.NewRequest("GET", apiBase+"/api/v1/directory", nil)
    req.Header.Set("x-api-key", apiKey)
    
    client := &http.Client{}
    resp, _ = client.Do(req)
    defer resp.Body.Close()
    
    body, _ := io.ReadAll(resp.Body)
    fmt.Println(string(body))
}
```

## Webhooks (Pro & Enterprise)

Configure webhooks to receive notifications when the directory is updated.

**Coming soon** - Contact contact@nexus-agi.com to be notified when available.

## Support

- **Free Tier**: Community support via GitHub Issues
- **Pro Tier**: Email support (24-48 hour response)
- **Enterprise Tier**: Priority email + Slack channel (4-hour response)

Contact: contact@nexus-agi.com

## Changelog

### Version 1.0.0 (2025-12-29)
- Initial API service release
- Three-tier pricing model (Free, Pro, Enterprise)
- Full directory access
- Search functionality
- Rate limiting
- Usage analytics
- API key management

## License

MIT License - Free to use with attribution

---

**Questions?** Email contact@nexus-agi.com or open an issue at github.com/nexus-agi-directory/nexus-agi-directory
