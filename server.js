const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const fs = require('fs').promises;
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Subscription tiers configuration
const TIERS = {
  free: {
    name: 'Free',
    rateLimit: 60, // requests per hour
    features: ['basic_directory', 'public_apis'],
    price: 0
  },
  pro: {
    name: 'Pro',
    rateLimit: 1000, // requests per hour
    features: ['basic_directory', 'public_apis', 'analytics', 'priority_support', 'webhooks'],
    price: 29 // per month
  },
  enterprise: {
    name: 'Enterprise',
    rateLimit: 10000, // requests per hour
    features: ['basic_directory', 'public_apis', 'analytics', 'priority_support', 'webhooks', 'custom_integration', 'sla'],
    price: 299 // per month
  }
};

// In-memory API key store (in production, use a database)
const API_KEYS = new Map();

// Initialize some demo API keys
API_KEYS.set('demo-free-key-12345', { tier: 'free', usage: 0, createdAt: new Date() });
API_KEYS.set('demo-pro-key-67890', { tier: 'pro', usage: 0, createdAt: new Date() });
API_KEYS.set('demo-enterprise-key-abcdef', { tier: 'enterprise', usage: 0, createdAt: new Date() });

// Authentication middleware
const authenticateApiKey = (req, res, next) => {
  const apiKey = req.headers['x-api-key'] || req.query.api_key;
  
  if (!apiKey) {
    // Allow free tier access without API key but with strict rate limits
    req.tier = 'free';
    req.authenticated = false;
    return next();
  }

  const keyData = API_KEYS.get(apiKey);
  if (!keyData) {
    return res.status(401).json({ error: 'Invalid API key' });
  }

  req.tier = keyData.tier;
  req.apiKey = apiKey;
  req.authenticated = true;
  req.keyData = keyData;
  next();
};

// Rate limiting based on tier
const createRateLimiter = (tier) => {
  const config = TIERS[tier];
  return rateLimit({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: config.rateLimit,
    message: {
      error: 'Rate limit exceeded',
      tier: tier,
      limit: config.rateLimit,
      upgrade: tier === 'free' ? 'Consider upgrading to Pro for higher limits' : null
    },
    standardHeaders: true,
    legacyHeaders: false,
  });
};

// Dynamic rate limiter middleware
const dynamicRateLimiter = (req, res, next) => {
  const tier = req.tier || 'free';
  const limiter = createRateLimiter(tier);
  limiter(req, res, next);
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    service: 'nexus-agi-directory'
  });
});

// API info endpoint
app.get('/api/v1/info', (req, res) => {
  res.json({
    name: 'Nexus AGI Directory API',
    version: '1.0.0',
    description: 'Machine-readable API discovery for autonomous agents',
    endpoints: {
      directory: '/api/v1/directory',
      search: '/api/v1/search',
      pricing: '/api/v1/pricing',
      register: '/api/v1/register'
    },
    authentication: 'API Key (x-api-key header or api_key query parameter)',
    documentation: 'https://nexus-agi.com/docs'
  });
});

// Pricing tiers endpoint
app.get('/api/v1/pricing', (req, res) => {
  res.json({
    tiers: Object.entries(TIERS).map(([key, value]) => ({
      id: key,
      ...value
    })),
    contact: 'contact@nexus-agi.com'
  });
});

// Main directory endpoint with authentication and rate limiting
app.get('/api/v1/directory', authenticateApiKey, dynamicRateLimiter, async (req, res) => {
  try {
    // Track usage
    if (req.authenticated && req.keyData) {
      req.keyData.usage++;
    }

    // Read the seeds-public.json file
    const filePath = path.join(__dirname, '.well-known', 'seeds-public.json');
    const data = await fs.readFile(filePath, 'utf-8');
    const directory = JSON.parse(data);

    // Add metadata
    const response = {
      meta: {
        tier: req.tier,
        authenticated: req.authenticated,
        count: directory.length,
        timestamp: new Date().toISOString(),
        rateLimit: {
          limit: TIERS[req.tier].rateLimit,
          remaining: res.getHeader('RateLimit-Remaining')
        }
      },
      data: directory
    };

    res.json(response);
  } catch (error) {
    console.error('Error reading directory:', error);
    res.status(500).json({ error: 'Failed to load directory' });
  }
});

// Search endpoint (premium feature)
app.get('/api/v1/search', authenticateApiKey, dynamicRateLimiter, async (req, res) => {
  const tier = req.tier;

  // Search is available to all tiers but with different result limits
  if (!req.authenticated && tier === 'free') {
    return res.status(403).json({ 
      error: 'Search requires authentication',
      message: 'Sign up for a free API key at nexus-agi.com/register'
    });
  }

  try {
    const { q, capability, status } = req.query;

    if (!q && !capability && !status) {
      return res.status(400).json({ error: 'Please provide at least one search parameter: q, capability, or status' });
    }

    const filePath = path.join(__dirname, '.well-known', 'seeds-public.json');
    const data = await fs.readFile(filePath, 'utf-8');
    let directory = JSON.parse(data);

    // Filter based on search criteria
    if (q) {
      const query = q.toLowerCase();
      directory = directory.filter(api => 
        api.name.toLowerCase().includes(query) ||
        api.id.toLowerCase().includes(query) ||
        (api.notes && api.notes.toLowerCase().includes(query))
      );
    }

    if (capability) {
      directory = directory.filter(api => 
        api.capabilities && api.capabilities.includes(capability)
      );
    }

    if (status) {
      directory = directory.filter(api => api.status === status);
    }

    // Limit results based on tier
    const resultLimits = { free: 10, pro: 50, enterprise: -1 };
    const limit = resultLimits[tier];
    if (limit > 0) {
      directory = directory.slice(0, limit);
    }

    res.json({
      meta: {
        tier: req.tier,
        query: { q, capability, status },
        count: directory.length,
        timestamp: new Date().toISOString()
      },
      data: directory
    });
  } catch (error) {
    console.error('Error searching directory:', error);
    res.status(500).json({ error: 'Search failed' });
  }
});

// API key registration endpoint (simplified - in production use proper auth)
app.post('/api/v1/register', express.json(), async (req, res) => {
  const { email, tier = 'free' } = req.body;

  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  if (!TIERS[tier]) {
    return res.status(400).json({ error: 'Invalid tier' });
  }

  // Generate API key
  const { v4: uuidv4 } = require('uuid');
  const apiKey = `nxs_${tier}_${uuidv4().replace(/-/g, '')}`;

  // Store the key
  API_KEYS.set(apiKey, {
    tier: tier,
    email: email,
    usage: 0,
    createdAt: new Date()
  });

  res.json({
    message: 'API key created successfully',
    apiKey: apiKey,
    tier: tier,
    tierDetails: TIERS[tier],
    usage: 'Include this key in x-api-key header or api_key query parameter',
    example: `curl -H "x-api-key: ${apiKey}" https://nexus-agi.com/api/v1/directory`
  });
});

// Usage analytics endpoint (premium feature)
app.get('/api/v1/analytics', authenticateApiKey, dynamicRateLimiter, (req, res) => {
  if (!req.authenticated) {
    return res.status(401).json({ error: 'Authentication required' });
  }

  const tier = req.tier;
  if (tier === 'free') {
    return res.status(403).json({ 
      error: 'Analytics not available on free tier',
      upgrade: 'Upgrade to Pro for analytics access'
    });
  }

  res.json({
    apiKey: req.apiKey.substring(0, 20) + '...',
    tier: tier,
    usage: req.keyData.usage,
    createdAt: req.keyData.createdAt,
    rateLimit: TIERS[tier].rateLimit,
    features: TIERS[tier].features
  });
});

// Serve static files from .well-known directory
app.use('/.well-known', express.static(path.join(__dirname, '.well-known')));

// Legacy endpoint for backward compatibility
app.get('/.well-known/seeds-public.json', async (req, res) => {
  try {
    const filePath = path.join(__dirname, '.well-known', 'seeds-public.json');
    const data = await fs.readFile(filePath, 'utf-8');
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to load directory' });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ 
    error: 'Not found',
    message: 'See /api/v1/info for available endpoints'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Nexus AGI Directory Service running on port ${PORT}`);
  console.log(`📚 API Info: http://localhost:${PORT}/api/v1/info`);
  console.log(`💰 Pricing: http://localhost:${PORT}/api/v1/pricing`);
  console.log(`🔑 Register: POST http://localhost:${PORT}/api/v1/register`);
});

module.exports = app;
