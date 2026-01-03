# Deployment Guide - Nexus AGI Directory Service

This guide covers deploying the Nexus AGI Directory API service to various platforms.

## Quick Start (Local Development)

### Prerequisites
- Node.js 18+ installed
- Git

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/DOUGLASDAVIS08161978/nexus-agi-directory.git
cd nexus-agi-directory
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env if needed
```

4. **Start the service**
```bash
npm start
```

The service will be available at `http://localhost:3000`

### Development Mode

For auto-reload during development:
```bash
npm run dev
```

## Docker Deployment

### Local Docker

1. **Build the image**
```bash
docker build -t nexus-agi-directory .
```

2. **Run the container**
```bash
docker run -p 3000:3000 \
  -e NODE_ENV=production \
  -v $(pwd)/.well-known:/app/.well-known:ro \
  nexus-agi-directory
```

### Docker Compose

For a complete stack with optional services:

```bash
docker-compose up -d
```

Access the API at `http://localhost:3000`

## Cloud Deployment Options

### Option 1: Vercel (Recommended for Serverless)

**Pros:** Free tier available, automatic HTTPS, global CDN
**Cons:** Cold starts, limited execution time

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Set environment variables**
```bash
vercel env add NODE_ENV production
```

4. **Production deployment**
```bash
vercel --prod
```

**Custom Domain:**
```bash
vercel domains add nexus-agi.com
```

### Option 2: Railway.app

**Pros:** Easy setup, free tier, automatic deployments
**Cons:** Limited free tier resources

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login and initialize**
```bash
railway login
railway init
```

3. **Deploy**
```bash
railway up
```

4. **Set environment variables**
```bash
railway variables set NODE_ENV=production
```

5. **Get your URL**
```bash
railway domain
```

### Option 3: Fly.io

**Pros:** Global distribution, reasonable pricing, Docker-based
**Cons:** Requires credit card

1. **Install Fly CLI**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login**
```bash
fly auth login
```

3. **Launch the app**
```bash
fly launch
```

4. **Deploy**
```bash
fly deploy
```

5. **Set secrets**
```bash
fly secrets set NODE_ENV=production
```

6. **Scale if needed**
```bash
fly scale count 2
fly scale memory 512
```

### Option 4: DigitalOcean App Platform

**Pros:** Managed service, predictable pricing
**Cons:** Higher cost than some alternatives

1. **Create a new app** at https://cloud.digitalocean.com/apps

2. **Connect your GitHub repository**

3. **Configure the app:**
   - Name: nexus-agi-directory
   - Region: Choose closest to users
   - Branch: main
   - Build Command: `npm install`
   - Run Command: `npm start`

4. **Set environment variables:**
   - `NODE_ENV=production`
   - `PORT=3000`

5. **Deploy**

### Option 5: AWS (Elastic Container Service)

**Pros:** Full control, scalable, production-ready
**Cons:** More complex, higher cost

1. **Push to ECR**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_URI
docker build -t nexus-agi-directory .
docker tag nexus-agi-directory:latest YOUR_ECR_URI/nexus-agi-directory:latest
docker push YOUR_ECR_URI/nexus-agi-directory:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "nexus-agi-directory",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "nexus-agi-directory",
      "image": "YOUR_ECR_URI/nexus-agi-directory:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        }
      ]
    }
  ]
}
```

3. **Create ECS Service with Load Balancer**

### Option 6: Heroku

**Pros:** Simple deployment, good for prototypes
**Cons:** Removed free tier, higher pricing

1. **Install Heroku CLI**
```bash
npm install -g heroku
```

2. **Login and create app**
```bash
heroku login
heroku create nexus-agi-directory
```

3. **Add buildpack**
```bash
heroku buildpacks:set heroku/nodejs
```

4. **Set environment variables**
```bash
heroku config:set NODE_ENV=production
```

5. **Deploy**
```bash
git push heroku main
```

## Production Configuration

### Environment Variables

Required variables for production:
```bash
NODE_ENV=production
PORT=3000
CONTACT_EMAIL=contact@nexus-agi.com
```

Optional (for enhanced features):
```bash
# Database
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Monitoring
SENTRY_DSN=https://...

# Email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email
SMTP_PASSWORD=your-password

# Payment (Stripe)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Security Checklist

- [ ] Use HTTPS in production
- [ ] Set secure environment variables
- [ ] Enable rate limiting
- [ ] Implement proper API key storage (database)
- [ ] Set up monitoring and alerts
- [ ] Configure CORS appropriately
- [ ] Enable security headers
- [ ] Set up automated backups
- [ ] Implement logging
- [ ] Use secrets management (AWS Secrets Manager, etc.)

### Performance Optimization

1. **Enable caching**
   - Cache API directory in Redis
   - Set Cache-Control headers
   - Use CDN for static assets

2. **Database optimization**
   - Use connection pooling
   - Index API keys table
   - Implement query optimization

3. **Monitoring**
   - Set up health checks
   - Monitor response times
   - Track error rates
   - Monitor rate limit usage

## Scaling

### Horizontal Scaling

Most platforms support auto-scaling:

**Vercel:** Automatic
**Railway:** Manual scaling via CLI
**Fly.io:** 
```bash
fly scale count 3
```

**AWS ECS:**
```bash
aws ecs update-service --service nexus-agi-directory --desired-count 3
```

### Vertical Scaling

Increase resources per instance:

**Fly.io:**
```bash
fly scale memory 1024
fly scale cpu 2
```

**Railway:**
```bash
railway resources set --memory 1024
```

## Monitoring & Logging

### Health Checks

All platforms should monitor: `GET /health`

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-29T23:00:00.000Z"
}
```

### Logging

Add structured logging for production:

```javascript
// Example with Winston
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### Monitoring Services

Recommended tools:
- **Sentry** - Error tracking
- **Datadog** - Full observability
- **New Relic** - Performance monitoring
- **LogDNA/LogTail** - Log aggregation

## Database Migration (Production)

For production, migrate from in-memory storage to PostgreSQL:

1. **Set up PostgreSQL**
```bash
# Using Docker
docker run -d \
  --name nexus-postgres \
  -e POSTGRES_DB=nexus_agi \
  -e POSTGRES_USER=nexus \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 \
  postgres:15-alpine
```

2. **Update server.js to use PostgreSQL**
```javascript
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});
```

3. **Create schema**
```sql
CREATE TABLE api_keys (
  id SERIAL PRIMARY KEY,
  key VARCHAR(255) UNIQUE NOT NULL,
  tier VARCHAR(50) NOT NULL,
  email VARCHAR(255),
  usage INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  last_used TIMESTAMP
);

CREATE INDEX idx_api_keys_key ON api_keys(key);
CREATE INDEX idx_api_keys_tier ON api_keys(tier);
```

## Custom Domain Setup

### DNS Configuration

Point your domain to your deployment:

**A Record:**
```
Type: A
Name: @
Value: YOUR_SERVER_IP
TTL: 3600
```

**CNAME (for subdomains):**
```
Type: CNAME
Name: api
Value: your-app.vercel.app
TTL: 3600
```

### SSL/TLS

Most platforms provide automatic HTTPS:
- **Vercel:** Automatic via Let's Encrypt
- **Railway:** Automatic
- **Fly.io:** Automatic
- **AWS:** Use ACM (AWS Certificate Manager)

## Backup & Disaster Recovery

### Backup Strategy

1. **Code:** Git repository (GitHub)
2. **Database:** Daily automated backups
3. **Configuration:** Store in version control
4. **Secrets:** Use secrets manager

### Example backup script:
```bash
#!/bin/bash
# backup-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="nexus_agi_backup_$DATE.sql"

pg_dump $DATABASE_URL > $BACKUP_FILE
aws s3 cp $BACKUP_FILE s3://nexus-agi-backups/
rm $BACKUP_FILE
```

## Cost Estimates

### Startup (Free Tier)
- **Vercel Free:** $0/month (hobby projects)
- **Railway Free:** $5/month credit (limited)
- **Fly.io:** ~$5/month (minimal resources)

### Small Scale (~1000 users)
- **Railway:** ~$20/month
- **DigitalOcean:** ~$25/month
- **Fly.io:** ~$30/month

### Medium Scale (~10000 users)
- **Railway:** ~$100/month
- **DigitalOcean:** ~$100/month
- **AWS ECS:** ~$150/month

### Large Scale (100000+ users)
- **AWS ECS/EKS:** $500-2000/month
- Includes: Load balancer, auto-scaling, RDS, Redis

## Troubleshooting

### Service won't start
```bash
# Check logs
docker logs nexus-agi-directory
# or
railway logs
# or
fly logs
```

### Rate limiting issues
- Check Redis connection
- Verify tier configuration
- Check for clock skew

### Database connection errors
- Verify DATABASE_URL
- Check firewall rules
- Ensure connection pooling

### High memory usage
- Implement caching
- Optimize JSON parsing
- Use streaming for large responses

## Next Steps

1. Deploy to chosen platform
2. Set up monitoring
3. Configure custom domain
4. Implement payment processing (Stripe)
5. Set up email notifications
6. Create admin dashboard
7. Implement analytics tracking
8. Add automated testing
9. Set up CI/CD pipeline
10. Document API for customers

## Support

For deployment assistance:
- Email: contact@nexus-agi.com
- GitHub Issues: github.com/nexus-agi-directory/nexus-agi-directory/issues

---

**Recommended Production Stack:**
- Platform: Vercel (API) + DigitalOcean (Database)
- Database: PostgreSQL on DigitalOcean
- Caching: Redis on Upstash
- Monitoring: Sentry
- Payments: Stripe
- Email: SendGrid or AWS SES
