# Alpha Vantage MCP Server Setup Guide

## Overview

This financial-advisor project uses the **Alpha Vantage MCP Server** to access real-time and historical stock market data. The MCP (Model Context Protocol) server enables our agents to fetch live market data, company information, news sentiment, and technical indicators.

## Alpha Vantage MCP Server Features

The Alpha Vantage MCP server provides 60+ tools across 9 categories:

| Category | Tools Used in This Project |
|----------|----------------------------|
| **Core Stock APIs** | GLOBAL_QUOTE, TIME_SERIES_DAILY, SYMBOL_SEARCH |
| **Alpha Intelligence** | NEWS_SENTIMENT, COMPANY_OVERVIEW |
| **Fundamental Data** | INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW |
| **Technical Indicators** | SMA, EMA, RSI, MACD (for strategy analysis) |

## Setup Instructions

### Step 1: Get Alpha Vantage API Key

1. Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Sign up for a free API key (supports 25 requests/day)
3. For production use, consider a premium plan:
   - Premium: 75 requests/minute, unlimited daily
   - Enterprise: Custom rate limits

### Step 2: Configure MCP Server Connection

There are two ways to use the Alpha Vantage MCP server:

#### Option A: Remote MCP Server (Recommended for Production)

Connect directly to Alpha Vantage's hosted MCP server:

```python
# Add to your .env file
ALPHA_VANTAGE_API_KEY=your_api_key_here
ALPHA_VANTAGE_MCP_URL=https://mcp.alphavantage.co/mcp
```

The MCP server will be accessed at: `https://mcp.alphavantage.co/mcp?apikey=YOUR_API_KEY`

#### Option B: Local MCP Server (for Development)

Install and run the Alpha Vantage MCP server locally:

```bash
# Install via uvx
uvx av-mcp YOUR_API_KEY

# Or install via npm
npm install -g @alphavantage/mcp-server
av-mcp YOUR_API_KEY
```

### Step 3: Update Environment Configuration

Update your `.env` file:

```env
# Existing Google Cloud Configuration
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=resolute-spirit-478702-n8
GOOGLE_CLOUD_LOCATION=us-east1
GOOGLE_CLOUD_STORAGE_BUCKET=financial-advisor-bucket-resolute-spirit-478702-n8

# Alpha Vantage MCP Server Configuration
ALPHA_VANTAGE_API_KEY=your_api_key_here
ALPHA_VANTAGE_MCP_URL=https://mcp.alphavantage.co/mcp
```

### Step 4: Verify MCP Server Connection

Test the connection:

```python
import os
from financial_advisor.tools import AlphaVantageTools

# Verify API key is loaded
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print(f"API Key loaded: {bool(api_key)}")

# Test tool availability
tools = AlphaVantageTools.get_all_alpha_vantage_tools()
print(f"Available tools: {len(tools)}")
for tool in tools:
    print(f"  - {tool.name}")
```

Expected output:
```
API Key loaded: True
Available tools: 6
  - alpha_vantage_global_quote
  - alpha_vantage_time_series_daily
  - alpha_vantage_symbol_search
  - alpha_vantage_company_overview
  - alpha_vantage_news_sentiment
  - alpha_vantage_sma
```

## Tool Usage in Agents

### Data Analyst Agent

The Data Analyst agent uses the following Alpha Vantage tools:

1. **alpha_vantage_global_quote**: Real-time stock price
   ```python
   {
     "symbol": "AAPL"
   }
   # Returns: Current price, change, volume, previous close
   ```

2. **alpha_vantage_company_overview**: Company fundamentals
   ```python
   {
     "symbol": "AAPL"
   }
   # Returns: Market cap, P/E, EPS, sector, dividend yield, etc.
   ```

3. **alpha_vantage_time_series_daily**: Historical prices
   ```python
   {
     "symbol": "AAPL",
     "outputsize": "compact"  # Last 100 data points
   }
   # Returns: OHLCV data for trend analysis
   ```

4. **alpha_vantage_symbol_search**: Find similar tickers
   ```python
   {
     "keywords": "technology stocks"
   }
   # Returns: List of matching ticker symbols
   ```

5. **alpha_vantage_news_sentiment**: News with sentiment scores
   ```python
   {
     "tickers": "AAPL",
     "limit": 50
   }
   # Returns: Recent news articles with sentiment analysis
   ```

### Trading Analyst Agent

The Trading Analyst uses market data from the Data Analyst but can also access technical indicators:

- **alpha_vantage_sma**: Simple Moving Average for trend analysis
- Additional indicators can be added from Alpha Vantage's 50+ technical indicator library

## API Rate Limits

| Plan | Rate Limit | Daily Limit | Cost |
|------|------------|-------------|------|
| Free | 25 requests/day | 25 | $0 |
| Premium | 75 requests/minute | Unlimited | $49.99/month |
| Enterprise | Custom | Unlimited | Custom pricing |

### Rate Limit Management

The project handles rate limits gracefully:

1. **Caching**: Market data is cached for 5 minutes to reduce API calls
2. **Retry Logic**: Automatic retry with exponential backoff on rate limit errors
3. **Fallback**: Falls back to Google Search if Alpha Vantage is unavailable

## Troubleshooting

### Common Issues

**1. "Invalid API Key" Error**
```bash
# Verify your API key is set correctly
echo $ALPHA_VANTAGE_API_KEY
# Update .env file with correct key
```

**2. "Rate Limit Exceeded" Error**
```bash
# Wait for rate limit to reset or upgrade to premium plan
# Check your usage at: https://www.alphavantage.co/account
```

**3. "MCP Server Connection Failed"**
```bash
# For remote server: Check internet connection
# For local server: Ensure av-mcp is running
# Check MCP server status: curl https://mcp.alphavantage.co/health
```

**4. "Tool Not Found" Error**
```python
# Verify tools are loaded correctly
from financial_advisor.tools import get_all_alpha_vantage_tools
tools = get_all_alpha_vantage_tools()
print([t.name for t in tools])
```

## Alternative MCP Servers

If Alpha Vantage doesn't meet your needs, consider these alternatives:

### 1. Financial Datasets MCP Server
- URL: `https://mcp.financialdatasets.ai/mcp`
- Features: SEC filings, financial statements, crypto data
- Free tier: 100 requests/day

### 2. EODHD MCP Server
- URL: `https://eodhd.com/financial-apis/mcp-server`
- Features: Global stock data, forex, commodities
- Free tier: 20 API calls/day

### 3. Yahoo Finance MCP Server
- Lightweight, no authentication required
- Good for basic stock quotes
- Limited to public data only

## Integration with Google ADK

The Alpha Vantage tools integrate seamlessly with Google ADK:

```python
from google.adk import Agent
from financial_advisor.tools import get_all_alpha_vantage_tools

# Create agent with Alpha Vantage tools
agent = Agent(
    model="gemini-2.5-pro",
    name="market_analyst",
    instruction="Analyze market data...",
    tools=get_all_alpha_vantage_tools(),
)
```

## Security Best Practices

1. **Never commit API keys** to version control
   ```bash
   # Ensure .env is in .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables** for all credentials
   ```python
   import os
   api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
   ```

3. **Rotate API keys** periodically (every 90 days recommended)

4. **Monitor usage** at [Alpha Vantage Dashboard](https://www.alphavantage.co/account)

## Support

For issues with:
- **Alpha Vantage MCP Server**: support@alphavantage.co
- **Financial Advisor Project**: Create an issue in this repository
- **Google ADK**: https://github.com/google/adk

## Additional Resources

- [Alpha Vantage Documentation](https://www.alphavantage.co/documentation/)
- [Alpha Vantage MCP Server Docs](https://mcp.alphavantage.co/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Google Agent Development Kit](https://cloud.google.com/vertex-ai/docs/agent-builder)
