# New AGI Endpoints Added - Quick Reference

## 📊 Summary

- **Total New Endpoints**: 16
- **Previous Count**: 143
- **New Total**: 159
- **Categories**: Ultra-fast, Cost-optimized, Specialized, Infrastructure, Enterprise, Multi-modal

---

## 🚀 Ultra-Fast Inference

### 1. Groq LPU Inference
- **ID**: `agi://service/groq/chat:v1`
- **Speed**: 700+ tokens/sec
- **Endpoint**: `https://api.groq.com/openai/v1/chat/completions`
- **Free Tier**: ✅ (14,400 requests/day)
- **Price**: $0.05/1M tokens
- **Models**: Llama 3, Mixtral, Gemma
- **Docs**: https://console.groq.com/docs/quickstart

### 2. Cerebras Inference
- **ID**: `agi://service/cerebras/chat:v1`
- **Speed**: 1800+ tokens/sec (world record)
- **Endpoint**: `https://api.cerebras.ai/v1/chat/completions`
- **Free Tier**: ❌
- **Price**: $0.60/1M tokens
- **Technology**: Wafer-scale engine
- **Status**: Beta
- **Docs**: https://inference-docs.cerebras.ai/

### 3. Fireworks AI
- **ID**: `agi://service/fireworks/chat:v1`
- **Speed**: Up to 4x faster than competitors
- **Endpoint**: `https://api.fireworks.ai/inference/v1/chat/completions`
- **Free Tier**: ✅
- **Price**: $0.20/1M tokens
- **Models**: Llama, Mixtral (optimized)
- **Docs**: https://docs.fireworks.ai/

---

## 💰 Cost-Optimized

### 4. Lepton AI
- **ID**: `agi://service/lepton/chat:v1`
- **Endpoint**: `https://api.lepton.ai/v1/chat/completions`
- **Free Tier**: ✅
- **Price**: $0.10/1M tokens (50% cheaper)
- **Models**: Llama, Mixtral
- **Docs**: https://docs.lepton.ai/

### 5. Together AI
- **ID**: `agi://service/together/chat:v1`
- **Endpoint**: `https://api.together.xyz/v1/chat/completions`
- **Free Tier**: ✅
- **Price**: $0.20/1M tokens
- **Models**: 100+ open-source models
- **Docs**: https://docs.together.ai/reference/chat-completions

### 6. OctoAI
- **ID**: `agi://service/octoai/chat:v1`
- **Endpoint**: `https://text.octoai.run/v1/chat/completions`
- **Free Tier**: ✅
- **Price**: $0.15/1M tokens
- **Specialty**: Custom fine-tuned models
- **Docs**: https://docs.octoai.cloud/

---

## 🧠 Specialized AI

### 7. DeepSeek
- **ID**: `agi://service/deepseek/chat:v1`
- **Endpoint**: `https://api.deepseek.com/v1/chat/completions`
- **Free Tier**: ✅
- **Price**: $0.14/1M tokens
- **Strength**: Coding & reasoning tasks
- **Models**: deepseek-chat, deepseek-coder
- **Docs**: https://platform.deepseek.com/api-docs

### 8. xAI Grok
- **ID**: `agi://service/xai/grok:v1`
- **Endpoint**: `https://api.x.ai/v1/chat/completions`
- **Free Tier**: ❌
- **Price**: $5.00/1M tokens
- **Specialty**: Real-time X (Twitter) data
- **Status**: Beta
- **Docs**: https://docs.x.ai/api

### 9. AI21 Labs Jurassic
- **ID**: `agi://service/ai21/chat:v1`
- **Endpoint**: `https://api.ai21.com/studio/v1/chat/completions`
- **Free Tier**: ✅
- **Price**: $0.80/1M tokens
- **Strength**: Multilingual support
- **Models**: Jamba (hybrid SSM-Transformer), Jurassic-2
- **Docs**: https://docs.ai21.com/

---

## 🔧 Infrastructure & Serverless

### 10. RunPod Serverless
- **ID**: `agi://service/runpod/serverless:v1`
- **Endpoint**: `https://api.runpod.ai/v2/{endpoint_id}/run`
- **Free Tier**: ❌
- **Price**: $0.0004/sec GPU (pay-per-second)
- **Specialty**: Deploy custom models on GPU
- **Supports**: Any ML framework
- **Docs**: https://docs.runpod.io/serverless/overview

### 11. Modal
- **ID**: `agi://service/modal/inference:v1`
- **Endpoint**: `https://api.modal.com/v1/web/{function_name}`
- **Free Tier**: ✅ ($30/month free credits)
- **Pricing**: Pay-per-second
- **Strength**: Python-first serverless
- **Features**: Auto-scaling, GPU support
- **Docs**: https://modal.com/docs/guide

### 12. Anyscale
- **ID**: `agi://service/anyscale/chat:v1`
- **Endpoint**: `https://api.endpoints.anyscale.com/v1/chat/completions`
- **Free Tier**: ✅
- **Price**: $0.15/1M tokens
- **Technology**: Built on Ray.io
- **Strength**: Production-ready scaling
- **Docs**: https://docs.anyscale.com/endpoints/

---

## 🏢 Enterprise Solutions

### 13. Writer (Palmyra)
- **ID**: `agi://service/writer/chat:v1`
- **Endpoint**: `https://api.writer.com/v1/chat/completions`
- **Free Tier**: ❌
- **Pricing**: Enterprise (contact sales)
- **Certification**: SOC2 Type II
- **Strength**: Data security & custom models
- **Docs**: https://dev.writer.com/

### 14. SambaNova Cloud
- **ID**: `agi://service/sambanova/chat:v1`
- **Endpoint**: `https://api.sambanova.ai/v1/chat/completions`
- **Free Tier**: ❌
- **Price**: $0.50/1M tokens
- **Technology**: Reconfigurable Dataflow Unit (RDU)
- **Status**: Beta
- **Focus**: Enterprise deployments
- **Docs**: https://docs.sambanova.ai/

---

## 🎨 Multi-Modal

### 15. Novita AI
- **ID**: `agi://service/novita/chat:v1`
- **Endpoint**: `https://api.novita.ai/v3/openai/chat/completions`
- **Free Tier**: ✅
- **Price**: $0.10/1M tokens
- **Capabilities**: Text, image, video generation
- **Models**: 100+ models
- **Docs**: https://docs.novita.ai/

### 16. Replicate LLM
- **ID**: `agi://service/replicate/llm:v1`
- **Endpoint**: `https://api.replicate.com/v1/predictions`
- **Free Tier**: ❌
- **Price**: $0.10/run
- **Strength**: Run any open model
- **Models**: 1000s available
- **Features**: Async predictions, webhooks
- **Docs**: https://replicate.com/docs/reference/http#predictions.create

---

## 🆕 New Capabilities Introduced

This update adds the following new capability tags to the directory:

- `ultra_fast` - Providers with >500 tokens/sec
- `wafer_scale` - Wafer-scale engine hardware (Cerebras)
- `dataflow_arch` - Dataflow architecture (SambaNova)
- `real_time` - Real-time data access (xAI)
- `x_integration` - X/Twitter platform integration
- `serverless` - Serverless deployment
- `gpu` - GPU-based inference
- `custom_models` - Custom model deployment support
- `custom_code` - Run arbitrary code (Modal)
- `cost_optimized` - Budget-friendly options
- `ray_backend` - Ray.io infrastructure
- `async_jobs` - Asynchronous predictions

---

## 📈 Impact by Category

| Category | Providers | Free Tier Available | Avg Price/1M Tokens |
|----------|-----------|---------------------|---------------------|
| Ultra-Fast | 3 | 2/3 (67%) | $0.28 |
| Cost-Optimized | 3 | 3/3 (100%) | $0.15 |
| Specialized | 3 | 2/3 (67%) | $1.98 |
| Infrastructure | 3 | 2/3 (67%) | Pay-per-use |
| Enterprise | 2 | 0/2 (0%) | Enterprise pricing |
| Multi-Modal | 2 | 1/2 (50%) | $0.10/run |

**Overall**: 10/16 (63%) offer free tiers

---

## 🔗 Quick Access

All endpoints are now accessible via the Nexus AGI Directory:

```bash
# Get all endpoints
curl https://nexus-agi.com/.well-known/seeds-public.json

# Filter for ultra-fast providers
curl https://nexus-agi.com/.well-known/seeds-public.json | \
  jq '.[] | select(.capabilities | contains(["ultra_fast"]))'

# Filter for free tier options
curl https://nexus-agi.com/.well-known/seeds-public.json | \
  jq '.[] | select(.pricing.free_tier == true)'
```

---

## 📝 Notes

- All endpoints follow OpenAI-compatible API format where applicable
- Auth methods properly documented (bearer tokens, API keys)
- Rate limits and pricing transparently listed
- Documentation links verified and current
- Status indicators accurate (stable/beta)

**Generated**: 2026-01-30
**Script**: `add_agi_endpoints.py`
**Branch**: `claude/audit-dependencies-mkobk7wfdv0lvds9-mimBO`
