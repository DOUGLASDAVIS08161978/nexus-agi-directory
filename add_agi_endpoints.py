#!/usr/bin/env python3
"""
Add Multiple AGI Endpoints to Nexus AGI Directory
Adds cutting-edge AI/ML API endpoints with proper formatting
"""

import json
from pathlib import Path
from datetime import datetime

# New AGI endpoints to add
NEW_ENDPOINTS = [
    {
        "id": "agi://service/deepseek/chat:v1",
        "name": "DeepSeek Chat API",
        "endpoint": "https://api.deepseek.com/v1/chat/completions",
        "capabilities": ["chat", "code", "reasoning", "stream"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${DEEPSEEK_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.14/1M tokens"},
        "docs": "https://platform.deepseek.com/api-docs",
        "status": "stable",
        "reputation": {"ecosystem": "emerging", "strength": "coding & reasoning"},
        "notes": "Strong performance on code and math tasks. Models: deepseek-chat, deepseek-coder"
    },
    {
        "id": "agi://service/groq/chat:v1",
        "name": "Groq LPU Inference",
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "capabilities": ["chat", "stream", "ultra_fast", "function_calling"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${GROQ_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "14,400 requests/day free tier"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.05/1M tokens"},
        "docs": "https://console.groq.com/docs/quickstart",
        "status": "stable",
        "reputation": {"ecosystem": "emerging", "strength": "ultra-fast inference (700+ tok/s)"},
        "notes": "Fastest inference available. Models: Llama 3, Mixtral, Gemma. OpenAI-compatible API."
    },
    {
        "id": "agi://service/together/chat:v1",
        "name": "Together AI Chat",
        "endpoint": "https://api.together.xyz/v1/chat/completions",
        "capabilities": ["chat", "code", "stream", "function_calling", "json_mode"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${TOGETHER_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.20/1M tokens"},
        "docs": "https://docs.together.ai/reference/chat-completions",
        "status": "stable",
        "reputation": {"ecosystem": "growing", "strength": "open models at scale"},
        "notes": "100+ open-source models. OpenAI-compatible. Fast inference on Llama, Mixtral, etc."
    },
    {
        "id": "agi://service/mistral/chat:v1",
        "name": "Mistral AI Chat",
        "endpoint": "https://api.mistral.ai/v1/chat/completions",
        "capabilities": ["chat", "function_calling", "stream", "json_mode"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${MISTRAL_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": False, "starting_price": "$0.25/1M tokens"},
        "docs": "https://docs.mistral.ai/api/",
        "status": "stable",
        "reputation": {"ecosystem": "established", "strength": "European AI leader"},
        "notes": "Models: Mistral Large, Mixtral 8x7B, Mistral 7B. OpenAI-compatible API."
    },
    {
        "id": "agi://service/perplexity/chat:v1",
        "name": "Perplexity AI Chat",
        "endpoint": "https://api.perplexity.ai/chat/completions",
        "capabilities": ["chat", "search", "citations", "stream"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${PERPLEXITY_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": False, "starting_price": "$1.00/1M tokens"},
        "docs": "https://docs.perplexity.ai/",
        "status": "stable",
        "reputation": {"ecosystem": "specialized", "strength": "real-time search + citations"},
        "notes": "Online models with built-in search. Models: pplx-70b-online, pplx-7b-online"
    },
    {
        "id": "agi://service/xai/grok:v1",
        "name": "xAI Grok API",
        "endpoint": "https://api.x.ai/v1/chat/completions",
        "capabilities": ["chat", "real_time", "stream", "x_integration"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${XAI_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": False, "starting_price": "$5.00/1M tokens"},
        "docs": "https://docs.x.ai/api",
        "status": "beta",
        "reputation": {"ecosystem": "emerging", "strength": "real-time X data access"},
        "notes": "Real-time access to X (Twitter) data. Models: grok-beta. OpenAI-compatible."
    },
    {
        "id": "agi://service/huggingface/inference:v1",
        "name": "Hugging Face Inference API",
        "endpoint": "https://api-inference.huggingface.co/models",
        "capabilities": ["text-gen", "embeddings", "classification", "image", "audio"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${HF_API_TOKEN}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model_path",
        "limits": {"rate": "1,000 requests/day free tier"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.06/1M tokens"},
        "docs": "https://huggingface.co/docs/api-inference/",
        "status": "stable",
        "reputation": {"ecosystem": "hub leader", "strength": "100k+ models available"},
        "notes": "Access 100k+ models. Append /{model-id} to endpoint. Serverless inference."
    },
    {
        "id": "agi://service/runpod/serverless:v1",
        "name": "RunPod Serverless",
        "endpoint": "https://api.runpod.ai/v2/{endpoint_id}/run",
        "capabilities": ["inference", "serverless", "gpu", "custom_models"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${RUNPOD_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "endpoint_id",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "pay-per-second", "free_tier": False, "starting_price": "$0.0004/sec GPU"},
        "docs": "https://docs.runpod.io/serverless/overview",
        "status": "stable",
        "reputation": {"ecosystem": "infrastructure", "strength": "custom GPU deployments"},
        "notes": "Deploy custom models on GPU. Pay per second. Supports any ML framework."
    },
    {
        "id": "agi://service/modal/inference:v1",
        "name": "Modal Inference",
        "endpoint": "https://api.modal.com/v1/web/{function_name}",
        "capabilities": ["inference", "serverless", "gpu", "custom_code"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${MODAL_TOKEN_ID}:${MODAL_TOKEN_SECRET}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "function_name",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "pay-per-second", "free_tier": True, "starting_price": "$30/month free credits"},
        "docs": "https://modal.com/docs/guide",
        "status": "stable",
        "reputation": {"ecosystem": "developer platform", "strength": "Python-first serverless"},
        "notes": "Deploy any Python code to GPU. Auto-scaling. Web endpoints for inference."
    },
    {
        "id": "agi://service/fireworks/chat:v1",
        "name": "Fireworks AI Chat",
        "endpoint": "https://api.fireworks.ai/inference/v1/chat/completions",
        "capabilities": ["chat", "function_calling", "stream", "ultra_fast"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${FIREWORKS_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.20/1M tokens"},
        "docs": "https://docs.fireworks.ai/",
        "status": "stable",
        "reputation": {"ecosystem": "performance leader", "strength": "fastest open models"},
        "notes": "Optimized inference for Llama, Mixtral, etc. Up to 4x faster than competitors."
    },
    {
        "id": "agi://service/anyscale/chat:v1",
        "name": "Anyscale Endpoints",
        "endpoint": "https://api.endpoints.anyscale.com/v1/chat/completions",
        "capabilities": ["chat", "stream", "function_calling", "ray_backend"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${ANYSCALE_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.15/1M tokens"},
        "docs": "https://docs.anyscale.com/endpoints/",
        "status": "stable",
        "reputation": {"ecosystem": "ray.io based", "strength": "scalable production inference"},
        "notes": "Built on Ray. Models: Llama 2/3, Mixtral, Mistral. Production-ready scaling."
    },
    {
        "id": "agi://service/ai21/chat:v1",
        "name": "AI21 Labs Jurassic",
        "endpoint": "https://api.ai21.com/studio/v1/chat/completions",
        "capabilities": ["chat", "stream", "multilingual"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${AI21_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.80/1M tokens"},
        "docs": "https://docs.ai21.com/",
        "status": "stable",
        "reputation": {"ecosystem": "established", "strength": "enterprise-grade multilingual"},
        "notes": "Models: Jamba (hybrid SSM-Transformer), Jurassic-2. Strong multilingual support."
    },
    {
        "id": "agi://service/writer/chat:v1",
        "name": "Writer (Palmyra)",
        "endpoint": "https://api.writer.com/v1/chat/completions",
        "capabilities": ["chat", "enterprise", "custom_models", "data_privacy"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${WRITER_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "enterprise"},
        "pricing": {"model": "enterprise", "free_tier": False, "starting_price": "Contact sales"},
        "docs": "https://dev.writer.com/",
        "status": "stable",
        "reputation": {"ecosystem": "enterprise", "strength": "data security & custom models"},
        "notes": "Palmyra models. Enterprise focus. Custom fine-tuning. SOC2 Type II certified."
    },
    {
        "id": "agi://service/replicate/llm:v1",
        "name": "Replicate LLM Inference",
        "endpoint": "https://api.replicate.com/v1/predictions",
        "capabilities": ["text-gen", "async_jobs", "open_models", "webhooks"],
        "auth": {"method": "bearer", "header": "Authorization: Token ${REPLICATE_API_TOKEN}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "version",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "pay-per-run", "free_tier": False, "starting_price": "$0.10/run"},
        "docs": "https://replicate.com/docs/reference/http#predictions.create",
        "status": "stable",
        "reputation": {"ecosystem": "model hub", "strength": "run any open model"},
        "notes": "Run 1000s of open models. Async predictions. Webhook callbacks. Pay per run."
    },
    {
        "id": "agi://service/lepton/chat:v1",
        "name": "Lepton AI",
        "endpoint": "https://api.lepton.ai/v1/chat/completions",
        "capabilities": ["chat", "stream", "cost_optimized"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${LEPTON_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.10/1M tokens"},
        "docs": "https://docs.lepton.ai/",
        "status": "stable",
        "reputation": {"ecosystem": "cost-optimized", "strength": "affordable inference"},
        "notes": "Low-cost inference. Models: Llama, Mixtral. 50% cheaper than major providers."
    },
    {
        "id": "agi://service/octoai/chat:v1",
        "name": "OctoAI Text Generation",
        "endpoint": "https://text.octoai.run/v1/chat/completions",
        "capabilities": ["chat", "stream", "custom_endpoints"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${OCTOAI_TOKEN}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.15/1M tokens"},
        "docs": "https://docs.octoai.cloud/",
        "status": "stable",
        "reputation": {"ecosystem": "optimization focused", "strength": "custom fine-tuned models"},
        "notes": "Optimized inference. Deploy custom models. OctoStack optimization platform."
    },
    {
        "id": "agi://service/openrouter/chat:v1",
        "name": "OpenRouter (Unified LLM Gateway)",
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "capabilities": ["chat", "stream", "multi_provider", "fallback", "routing"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${OPENROUTER_API_KEY}"},
        "headers": {"Content-Type": "application/json", "HTTP-Referer": "${YOUR_SITE_URL}"},
        "models_param": "model",
        "limits": {"rate": "by provider"},
        "pricing": {"model": "passthrough", "free_tier": True, "starting_price": "varies by model"},
        "docs": "https://openrouter.ai/docs",
        "status": "stable",
        "reputation": {"ecosystem": "aggregator", "strength": "100+ models, one API"},
        "notes": "Access GPT-4, Claude, Llama, etc. via one API. Automatic fallbacks. Cost tracking."
    },
    {
        "id": "agi://service/cerebras/chat:v1",
        "name": "Cerebras Inference",
        "endpoint": "https://api.cerebras.ai/v1/chat/completions",
        "capabilities": ["chat", "stream", "ultra_fast", "wafer_scale"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${CEREBRAS_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": False, "starting_price": "$0.60/1M tokens"},
        "docs": "https://inference-docs.cerebras.ai/",
        "status": "beta",
        "reputation": {"ecosystem": "hardware innovator", "strength": "world's fastest inference"},
        "notes": "Wafer-scale engine. 1800+ tokens/sec. Models: Llama 3. Record-breaking speeds."
    },
    {
        "id": "agi://service/sambanova/chat:v1",
        "name": "SambaNova Cloud",
        "endpoint": "https://api.sambanova.ai/v1/chat/completions",
        "capabilities": ["chat", "stream", "dataflow_arch"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${SAMBANOVA_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": False, "starting_price": "$0.50/1M tokens"},
        "docs": "https://docs.sambanova.ai/",
        "status": "beta",
        "reputation": {"ecosystem": "hardware + software", "strength": "dataflow architecture"},
        "notes": "Reconfigurable Dataflow Unit (RDU). Optimized for large models. Enterprise focus."
    },
    {
        "id": "agi://service/novita/chat:v1",
        "name": "Novita AI",
        "endpoint": "https://api.novita.ai/v3/openai/chat/completions",
        "capabilities": ["chat", "image", "video", "multi_modal"],
        "auth": {"method": "bearer", "header": "Authorization: Bearer ${NOVITA_API_KEY}"},
        "headers": {"Content-Type": "application/json"},
        "models_param": "model",
        "limits": {"rate": "by plan"},
        "pricing": {"model": "usage-based", "free_tier": True, "starting_price": "$0.10/1M tokens"},
        "docs": "https://docs.novita.ai/",
        "status": "stable",
        "reputation": {"ecosystem": "multi-modal", "strength": "unified text/image/video API"},
        "notes": "Text, image, video generation. 100+ models. OpenAI-compatible. Pay-as-you-go."
    }
]

def add_endpoints_to_directory():
    """Add new AGI endpoints to the Nexus AGI Directory"""

    seeds_file = Path('.well-known/seeds-public.json')

    if not seeds_file.exists():
        print(f"❌ ERROR: {seeds_file} not found!")
        print("Make sure you're running this from the nexus-agi-directory root")
        return False

    print("=" * 80)
    print("Adding Multiple AGI Endpoints to Nexus AGI Directory")
    print("=" * 80)
    print()

    # Load existing directory
    print(f"Loading {seeds_file}...")
    with open(seeds_file, 'r') as f:
        directory = json.load(f)

    print(f"✅ Current directory has {len(directory)} endpoints")
    print()

    # Get existing IDs to avoid duplicates
    existing_ids = {entry['id'] for entry in directory}

    # Add new endpoints
    added_count = 0
    skipped_count = 0

    print("Adding new endpoints:")
    print("-" * 80)

    for endpoint in NEW_ENDPOINTS:
        if endpoint['id'] in existing_ids:
            print(f"⏭️  Skipped (exists): {endpoint['name']}")
            skipped_count += 1
        else:
            directory.append(endpoint)
            print(f"✅ Added: {endpoint['name']}")
            print(f"   ID: {endpoint['id']}")
            print(f"   Endpoint: {endpoint['endpoint']}")
            print(f"   Capabilities: {', '.join(endpoint['capabilities'])}")
            print()
            added_count += 1

    print("-" * 80)
    print()

    if added_count == 0:
        print("ℹ️  No new endpoints added (all already exist)")
        return True

    # Save updated directory
    print(f"Saving updated directory ({len(directory)} total endpoints)...")

    # Create backup
    backup_file = seeds_file.with_suffix('.json.backup')
    with open(backup_file, 'w') as f:
        json.dump(directory, f, indent=2, ensure_ascii=False)
    print(f"✅ Backup saved: {backup_file}")

    # Save updated file
    with open(seeds_file, 'w') as f:
        json.dump(directory, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated {seeds_file}")
    print()

    print("=" * 80)
    print("✅ SUCCESS!")
    print("=" * 80)
    print()
    print(f"📊 Summary:")
    print(f"   New endpoints added: {added_count}")
    print(f"   Skipped (duplicates): {skipped_count}")
    print(f"   Total endpoints now: {len(directory)}")
    print()

    print("📝 New providers added:")
    for endpoint in NEW_ENDPOINTS:
        if endpoint['id'] not in existing_ids:
            print(f"   • {endpoint['name']} - {endpoint['reputation']['strength']}")

    print()
    print("🔄 Next steps:")
    print("   1. Review changes: git diff .well-known/seeds-public.json")
    print("   2. Test the file: python3 -m json.tool .well-known/seeds-public.json > /dev/null")
    print("   3. Commit: git add .well-known/seeds-public.json")
    print("   4. Create PR to nexus-agi-directory")
    print()

    return True

if __name__ == "__main__":
    success = add_endpoints_to_directory()
    exit(0 if success else 1)
