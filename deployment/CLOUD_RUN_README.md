# Cloud Run Deployment Guide

## Overview

Deploy the Financial Advisor agent to Google Cloud Run - a fully managed serverless platform that automatically scales your containerized application.

### Why Cloud Run?

✅ **Works with MCP Tools** - Full control over environment and dependencies
✅ **Easy Environment Variables** - Pass `ALPHA_VANTAGE_API_KEY` at deployment time
✅ **Auto-scaling** - Scales to zero when not in use, saves costs
✅ **Fast Deployment** - Typically completes in 3-5 minutes
✅ **HTTP/REST API** - Easy to integrate with any application

## Prerequisites

1. **Google Cloud Project** with billing enabled
2. **Enable Required APIs**:
   ```bash
   gcloud services enable \
     cloudbuild.googleapis.com \
     run.googleapis.com \
     artifactregistry.googleapis.com
   ```

3. **Environment Variables** in `.env` file:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ALPHA_VANTAGE_API_KEY=your-api-key
   ```

## Quick Start Deployment

### Option 1: Using the Deployment Script (Recommended)

```bash
# From project root:
./deployment/deploy_cloud_run.sh
```

This script will:
1. Build a Docker container with your agent
2. Push it to Google Container Registry
3. Deploy to Cloud Run with environment variables configured
4. Output the service URL

### Option 2: Manual Deployment

```bash
# 1. Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# 2. Build the container
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/financial-advisor

# 3. Deploy to Cloud Run
gcloud run deploy financial-advisor \
  --image=gcr.io/${GOOGLE_CLOUD_PROJECT}/financial-advisor \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --timeout=300 \
  --set-env-vars="ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY}" \
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=1"
```

## Testing Your Deployment

Once deployed, you'll receive a service URL like: `https://financial-advisor-xxx-uc.a.run.app`

### Test the API

```bash
# Health check
curl https://YOUR_SERVICE_URL/health

# API Documentation (interactive)
open https://YOUR_SERVICE_URL/docs

# Query the agent
curl -X POST https://YOUR_SERVICE_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze AAPL stock",
    "session_id": "test-session"
  }'
```

## API Endpoints

### GET `/`
Root endpoint with API information

### GET `/health`
Health check endpoint
```json
{
  "status": "healthy",
  "service": "financial-advisor",
  "version": "0.1.0"
}
```

### GET `/docs`
Interactive API documentation (Swagger UI)

### POST `/query`
Query the financial advisor agent

**Request Body:**
```json
{
  "query": "Analyze AAPL stock for conservative investor",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "result": "...",
  "session_id": "...",
  "metadata": {}
}
```

## Configuration

### Environment Variables

Set these when deploying:

- `ALPHA_VANTAGE_API_KEY` - Your Alpha Vantage API key (required)
- `GOOGLE_GENAI_USE_VERTEXAI` - Set to "1" to use Vertex AI
- `AGENT_VERSION` - Version tag for your deployment
- `COMMIT_SHA` - Git commit SHA for tracking

### Resource Configuration

Adjust based on your needs:

```bash
--memory=2Gi          # Memory allocation (512Mi to 32Gi)
--cpu=2               # CPU cores (1 to 8)
--timeout=300         # Request timeout in seconds
--max-instances=10    # Maximum concurrent instances
--min-instances=0     # Minimum instances (0 for cost savings)
```

## Cost Optimization

### Pay-Per-Use Pricing
Cloud Run charges only for:
- CPU and memory used during request handling
- Number of requests

### Estimated Costs (us-central1)
- **Idle**: $0/month (scales to zero)
- **Light usage** (100 requests/day): ~$5-10/month
- **Moderate usage** (1000 requests/day): ~$30-50/month

### Cost Saving Tips
1. Set `--min-instances=0` to scale to zero when idle
2. Use `--memory=1Gi` if 2Gi is too much
3. Set up alerts for unexpected usage

## Monitoring and Logs

### View Logs
```bash
# Real-time logs
gcloud run services logs tail financial-advisor \
  --region=us-central1

# Recent logs in Cloud Console
gcloud run services logs read financial-advisor \
  --region=us-central1 \
  --limit=100
```

### Metrics Dashboard
View in Cloud Console:
```
https://console.cloud.google.com/run/detail/us-central1/financial-advisor/metrics
```

## Updating Your Deployment

### Redeploy with Changes

```bash
# Just run the deployment script again
./deployment/deploy_cloud_run.sh
```

Cloud Run will:
1. Build a new container image
2. Deploy with zero downtime
3. Automatically route traffic to the new version

### Rollback to Previous Version

```bash
gcloud run services update-traffic financial-advisor \
  --to-revisions=PREVIOUS_REVISION=100 \
  --region=us-central1
```

## Troubleshooting

### Deployment Fails

**Issue**: "Container failed to start"
- Check logs: `gcloud run services logs tail financial-advisor`
- Common causes:
  - Missing environment variables
  - Port mismatch (must be 8080)
  - Import errors

**Issue**: "Permission denied"
- Ensure Cloud Build API is enabled
- Check IAM permissions for your account

### Runtime Issues

**Issue**: "API rate limit exceeded"
- Your ALPHA_VANTAGE_API_KEY may have hit rate limits
- Check usage at https://www.alphavantage.co/

**Issue**: "Timeout errors"
- Increase timeout: `--timeout=600`
- Check agent performance in logs

### Cold Starts

Cloud Run may have cold starts (1-3 seconds) when scaling from zero.

**Solution**: Set minimum instances
```bash
--min-instances=1  # Keeps one instance warm
```

## Security

### Authentication

The deployment script uses `--allow-unauthenticated` for easy testing.

**For production**, enable authentication:

```bash
gcloud run deploy financial-advisor \
  --no-allow-unauthenticated \
  ...
```

Then use authenticated requests:
```bash
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  https://YOUR_SERVICE_URL/query
```

### API Keys

Never commit `.env` file to git. The deployment script reads from `.env` and passes environment variables securely.

## Comparison: Cloud Run vs Agent Engine

| Feature | Cloud Run | Agent Engine |
|---------|-----------|--------------|
| MCP Tool Support | ✅ Full support | ❌ Limited |
| Environment Variables | ✅ Easy | ⚠️ Manual config |
| Deployment Time | 3-5 minutes | 5-10 minutes |
| Cost (idle) | $0 | ~$0.10/hour |
| Scaling | Automatic | Managed |
| Control | Full | Limited |

**Recommendation**: Use Cloud Run for this project due to MCP tool requirements.

## Next Steps

1. **Deploy**: Run `./deployment/deploy_cloud_run.sh`
2. **Test**: Try the `/docs` endpoint for interactive testing
3. **Integrate**: Use the REST API in your application
4. **Monitor**: Set up alerts and logging
5. **Optimize**: Adjust resources based on usage patterns
