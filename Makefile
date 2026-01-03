.PHONY: help install start dev test build docker-build docker-run docker-compose-up docker-compose-down deploy-vercel deploy-railway deploy-fly clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	npm install

start: ## Start the service in production mode
	npm start

dev: ## Start the service in development mode with auto-reload
	npm run dev

test: ## Run tests
	npm test

build: ## Build the Docker image
	docker build -t nexus-agi-directory .

docker-run: build ## Build and run Docker container
	docker run -p 3000:3000 \
		-e NODE_ENV=production \
		-v $$(pwd)/.well-known:/app/.well-known:ro \
		nexus-agi-directory

docker-compose-up: ## Start services with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop services with docker-compose
	docker-compose down

docker-compose-logs: ## Show docker-compose logs
	docker-compose logs -f

deploy-vercel: ## Deploy to Vercel
	vercel --prod

deploy-railway: ## Deploy to Railway
	railway up

deploy-fly: ## Deploy to Fly.io
	fly deploy

clean: ## Clean up generated files
	rm -rf node_modules
	rm -rf dist
	rm -rf tmp

health-check: ## Check if service is healthy
	@curl -s http://localhost:3000/health | jq .

api-info: ## Get API information
	@curl -s http://localhost:3000/api/v1/info | jq .

pricing: ## Show pricing tiers
	@curl -s http://localhost:3000/api/v1/pricing | jq .

register-demo: ## Register a demo API key
	@curl -X POST http://localhost:3000/api/v1/register \
		-H "Content-Type: application/json" \
		-d '{"email":"demo@example.com","tier":"free"}' | jq .

.DEFAULT_GOAL := help
