#!/bin/bash
#
# Trigger Google Cloud Build to deploy tBTC token
#

set -e

echo "🚀 TRIGGERING GOOGLE CLOUD BUILD - tBTC DEPLOYMENT"
echo "================================================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ ERROR: gcloud CLI not found!"
    echo ""
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "❌ ERROR: Not authenticated with gcloud"
    echo ""
    echo "Run: gcloud auth login"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ ERROR: No active GCP project"
    echo ""
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "Project: $PROJECT_ID"
echo ""

# Check if APIs are enabled
echo "📋 Checking required APIs..."

REQUIRED_APIS=(
    "cloudbuild.googleapis.com"
    "secretmanager.googleapis.com"
)

for API in "${REQUIRED_APIS[@]}"; do
    if gcloud services list --enabled --filter="name:$API" --format="value(name)" | grep -q "$API"; then
        echo "  ✅ $API"
    else
        echo "  ❌ $API (not enabled)"
        echo ""
        echo "Enable with: gcloud services enable $API"
        exit 1
    fi
done

echo ""
echo "🔐 Checking secret..."

# Check if secret exists
if gcloud secrets describe base-sepolia-private-key &> /dev/null; then
    echo "  ✅ Secret 'base-sepolia-private-key' exists"
else
    echo "  ❌ Secret 'base-sepolia-private-key' not found"
    echo ""
    echo "Create with:"
    echo "  echo -n 'YOUR_PRIVATE_KEY' | gcloud secrets create base-sepolia-private-key --data-file=-"
    exit 1
fi

echo ""
echo "📦 Checking storage bucket..."

BUCKET_NAME="${PROJECT_ID}_cloudbuild"

if gsutil ls -b "gs://${BUCKET_NAME}" &> /dev/null; then
    echo "  ✅ Bucket gs://${BUCKET_NAME} exists"
else
    echo "  ⚠️  Creating bucket gs://${BUCKET_NAME}..."
    gsutil mb "gs://${BUCKET_NAME}"
    echo "  ✅ Bucket created"
fi

echo ""
echo "================================================================"
echo "🚀 SUBMITTING BUILD TO GOOGLE CLOUD"
echo "================================================================"
echo ""

# Submit build
gcloud builds submit --config=cloudbuild.yaml .

echo ""
echo "================================================================"
echo "✅ BUILD SUBMITTED!"
echo "================================================================"
echo ""
echo "View logs:"
echo "  gcloud builds list --limit=1"
echo "  gcloud builds log \$(gcloud builds list --limit=1 --format='value(id)')"
echo ""
echo "View output:"
echo "  gsutil cat gs://${BUCKET_NAME}/deployments/deployment_output.txt"
echo ""
