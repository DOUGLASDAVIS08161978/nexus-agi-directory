# Google Cloud Build - tBTC Token Deployment

## Prerequisites

1. **Google Cloud Project** with billing enabled
2. **Cloud Build API** enabled
3. **Secret Manager API** enabled
4. **gcloud CLI** installed and authenticated

## Setup Instructions

### 1. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 2. Create Secret for Private Key

```bash
# Create the secret
echo -n "0eee6f45b0af8f5a6a24744a1a978346d5bd66b41c64dc30bd18a32e246515cd" | \
  gcloud secrets create base-sepolia-private-key \
  --data-file=- \
  --replication-policy="automatic"

# Grant Cloud Build access to the secret
PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")

gcloud secrets add-iam-policy-binding base-sepolia-private-key \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 3. Create Storage Bucket (for artifacts)

```bash
PROJECT_ID=$(gcloud config get-value project)
gsutil mb gs://${PROJECT_ID}_cloudbuild
```

### 4. Deploy tBTC Token

```bash
# From the repository root
gcloud builds submit --config=cloudbuild.yaml .
```

## Alternative: Manual Trigger

```bash
# Using the trigger script
./trigger_cloud_build.sh
```

## View Build Logs

```bash
# List recent builds
gcloud builds list --limit=5

# View specific build
gcloud builds log <BUILD_ID>
```

## View Deployment Output

```bash
PROJECT_ID=$(gcloud config get-value project)
gsutil cat gs://${PROJECT_ID}_cloudbuild/deployments/deployment_output.txt
```

## Cost Estimate

- **Cloud Build**: ~$0.003 per build minute (120 free build-minutes/day)
- **Secret Manager**: $0.06 per secret per month + $0.03 per 10,000 access operations
- **Storage**: ~$0.026 per GB per month

**Estimated cost per deployment**: < $0.01

## Security Notes

- ✅ Private key stored in **Secret Manager** (encrypted at rest)
- ✅ Not exposed in logs or build configuration
- ✅ Automatic IAM-based access control
- ✅ Audit logging enabled by default

## Troubleshooting

### Error: "Permission denied on secret"

```bash
# Re-grant access to Cloud Build service account
PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding base-sepolia-private-key \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Error: "API not enabled"

```bash
gcloud services enable cloudbuild.googleapis.com secretmanager.googleapis.com
```

### Error: "Bucket does not exist"

```bash
PROJECT_ID=$(gcloud config get-value project)
gsutil mb gs://${PROJECT_ID}_cloudbuild
```
