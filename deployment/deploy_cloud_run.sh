#!/bin/bash
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Deploy Financial Advisor to Cloud Run

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT}
REGION=${GOOGLE_CLOUD_LOCATION:-us-east1}
SERVICE_NAME="financial-advisor"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
ALPHA_VANTAGE_KEY=${ALPHA_VANTAGE_API_KEY}

# Validate required variables
if [ -z "$PROJECT_ID" ]; then
    echo "Error: GOOGLE_CLOUD_PROJECT is not set"
    exit 1
fi

if [ -z "$ALPHA_VANTAGE_KEY" ]; then
    echo "Error: ALPHA_VANTAGE_API_KEY is not set"
    exit 1
fi

# Set the active project
echo "Setting active project to: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# Check if required APIs are enabled
echo ""
echo "Checking required APIs..."
REQUIRED_APIS=("cloudbuild.googleapis.com" "run.googleapis.com" "artifactregistry.googleapis.com")

for api in "${REQUIRED_APIS[@]}"; do
    if gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
        echo "✓ $api is enabled"
    else
        echo "✗ $api is NOT enabled. Enabling now..."
        gcloud services enable "$api" --project="$PROJECT_ID"
        echo "✓ $api enabled"
    fi
done

echo "======================================"
echo "Deploying Financial Advisor to Cloud Run"
echo "======================================"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo "======================================"

# Build the container image
echo ""
echo "Step 1: Building container image..."
gcloud builds submit --tag "${IMAGE_NAME}" --project="${PROJECT_ID}"

# Deploy to Cloud Run
echo ""
echo "Step 2: Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
    --image="${IMAGE_NAME}" \
    --platform=managed \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --allow-unauthenticated \
    --memory=2Gi \
    --cpu=2 \
    --timeout=300 \
    --min-instances=0 \
    --max-instances=10 \
    --set-env-vars="ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_KEY}" \
    --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=1"

# Get the service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
    --platform=managed \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --format="value(status.url)")

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo "Service URL: ${SERVICE_URL}"
echo "Health Check: ${SERVICE_URL}/health"
echo "API Docs: ${SERVICE_URL}/docs"
echo "======================================"
