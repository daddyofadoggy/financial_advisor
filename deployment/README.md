# Deployment Instructions for Financial Advisor Agent

## Prerequisites

1. **Google Cloud Project Setup**
   - Enable the following APIs in your GCP project:
     - Vertex AI API
     - Agent Engine API
     - Cloud Storage API

2. **Environment Variables**
   - Set up `.env` file in the project root with:
     ```
     GOOGLE_CLOUD_PROJECT=your-project-id
     GOOGLE_CLOUD_LOCATION=us-central1  # Must be us-central1 for Agent Engines
     GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
     ALPHA_VANTAGE_API_KEY=your-api-key
     ```

3. **Install Dependencies**
   ```bash
   uv pip install -e .
   uv pip install fpdf2 matplotlib
   ```

## Deployment Commands

### Create a New Agent Engine

```bash
# From the project root directory:
PYTHONPATH=. python deployment/deploy.py --create
```

### List All Deployed Agents

```bash
PYTHONPATH=. python deployment/deploy.py --list
```

### Delete an Agent Engine

```bash
PYTHONPATH=. python deployment/deploy.py --delete --resource_id="projects/PROJECT_ID/locations/LOCATION/reasoningEngines/ENGINE_ID"
```

## Important Notes

### Region Support
- Agent Engines is **only available in specific regions**
- Currently using: `us-central1`
- Do NOT use: `us-east1` (not supported)

### Environment Variables in Deployed Agent
Currently, Agent Engines does not support passing environment variables directly through the deployment API.

**After deployment**, you need to configure the `ALPHA_VANTAGE_API_KEY` manually:
- Option 1: Through Google Cloud Console (Vertex AI > Agent Builder)
- Option 2: Use Google Secret Manager and update your agent code to fetch secrets at runtime

Your API Key: Check `.env` file for `ALPHA_VANTAGE_API_KEY` value

### Deployment Takes Time
- Agent Engine creation typically takes 5-10 minutes
- The script will wait and display progress
- You can also monitor logs at: https://console.cloud.google.com/logs/query?project=YOUR_PROJECT_ID

## Troubleshooting

### ModuleNotFoundError: No module named 'financial_advisor'
**Solution**: Always run deployment with `PYTHONPATH=.` prefix:
```bash
PYTHONPATH=. python deployment/deploy.py --create
```

### Model Not Found (404 errors)
**Solution**: Ensure you're using `gemini-2.5-pro` model. Some models are not available in all regions.

### Region Not Supported
**Solution**: Change `GOOGLE_CLOUD_LOCATION` to `us-central1` in your `.env` file

### Agent Engine Failed to Start
**Possible causes**:
1. Missing environment variables (ALPHA_VANTAGE_API_KEY)
2. Import errors in agent code
3. Invalid dependencies

**Solution**: Check Cloud Logging for detailed error messages:
```bash
# View logs in Cloud Console
https://console.cloud.google.com/logs/query?project=YOUR_PROJECT_ID
```

## Cost Estimates

- Agent Engine hosting: ~$0.10 per hour while running
- Gemini API calls: Per-token pricing
- Cloud Storage: Minimal (~$0.01/month for agent artifacts)

Consider deleting test deployments when not in use to minimize costs.

## Files Modified for Deployment

### Key Changes Made:

1. **`financial_advisor/tools/alpha_vantage_tools.py`**
   - Added `LazyMCPToolset` wrapper class
   - Made MCP toolset picklable for Agent Engines deployment
   - Added graceful handling for missing API keys

2. **`deployment/deploy.py`**
   - Updated requirements to include `fpdf2`, `matplotlib`, `python-dotenv`
   - Added deployment notes and instructions
   - Configured for `us-central1` region

3. **`.env`**
   - Changed location from `us-east1` to `us-central1`

## Next Steps After Deployment

1. Configure `ALPHA_VANTAGE_API_KEY` in the deployed agent
2. Test the agent through the Agent Builder UI
3. Integrate with your application using the Agent Engine API
4. Monitor usage and costs through Cloud Console
