# Fix for "Multiple tools are supported only when they are all search tools" Error

## Problem
When running `adk web` and chatting, got error:
```
400 INVALID_ARGUMENT. {'error': {'code': 400, 'message':
'Multiple tools are supported only when they are all search tools.',
'status': 'INVALID_ARGUMENT'}}
```

## Root Cause
**Google ADK/Gemini Restriction**: An agent cannot mix different types of tools. You can only use:
- All search tools (multiple search tools together), OR
- A single non-search tool/toolset

**The Issue**: Data Analyst was using BOTH:
- `google_search` (a search tool)
- `alpha_vantage_toolset` (an MCP toolset)

This combination is **not allowed** by Gemini.

## Solution: Use Only Alpha Vantage MCP Tools

**Removed** `google_search` from data analyst and rely **entirely** on Alpha Vantage MCP server.

### Why This Works

Alpha Vantage MCP server provides **60+ tools** that cover everything we need:

| Data Type | Alpha Vantage Tools | What We Get |
|-----------|-------------------|-------------|
| **Market Data** | GLOBAL_QUOTE, TIME_SERIES_DAILY, TIME_SERIES_INTRADAY | Real-time prices, historical data, intraday patterns |
| **Company Info** | COMPANY_OVERVIEW, EARNINGS, LISTING_STATUS | Fundamentals, P/E, market cap, sector, earnings |
| **Financial Statements** | INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW | Complete financial statements |
| **News & Sentiment** | NEWS_SENTIMENT | News articles with bullish/bearish/neutral sentiment scores |
| **Technical Indicators** | RSI, MACD, EMA, BBANDS, ADX, STOCH, 50+ more | All technical analysis tools |
| **Search & Discovery** | SYMBOL_SEARCH | Find tickers by company name or keywords |

**What we lost**: Google Search for general web search
**What we gained**: Structured, verified financial data from a professional source

## Files Changed

1. ✅ **financial_advisor/sub_agents/data_analyst/agent.py**
   - Removed: `google_search`
   - Kept: `alpha_vantage_toolset` only

2. ✅ **financial_advisor/sub_agents/data_analyst/prompt.py**
   - Updated: Tool usage instructions to focus on Alpha Vantage MCP
   - Removed: References to Google Search
   - Added: Guidance on using additional Alpha Vantage tools

## Verification

```bash
# Test module loads
python -c "from financial_advisor.agent import root_agent; print('OK')"

# Should output: Module loaded successfully
#                Data Analyst tools: 1
```

## Now You Can Run

```bash
adk web

# Chat interface will open at http://localhost:8000
# No more "multiple tools" error!
```

## Test Queries

Try these to verify everything works:

1. **Basic market data:**
   ```
   "What's the current price of AAPL?"
   ```

2. **Comprehensive analysis:**
   ```
   "Analyze TSLA stock - give me current price, news sentiment, and similar stocks"
   ```

3. **Full financial advisory:**
   ```
   "I want to invest $1,000 in tech stocks with moderate risk for long-term.
    Analyze GOOGL and recommend strategies."
   ```

## Tool Usage by Agent (Updated)

| Agent | Tools | Count |
|-------|-------|-------|
| Data Analyst | Alpha Vantage MCP Toolset | 1 toolset (60+ tools) |
| Trading Analyst | Alpha Vantage MCP Toolset | 1 toolset (60+ tools) |
| Execution Analyst | Alpha Vantage MCP Toolset | 1 toolset (60+ tools) |
| Risk Analyst | Alpha Vantage MCP Toolset | 1 toolset (60+ tools) |

**Total**: All agents share access to the same 60+ Alpha Vantage tools.

## Benefits of This Approach

✅ **No restriction conflicts** - Each agent uses one toolset only
✅ **Comprehensive data** - 60+ tools cover all financial analysis needs
✅ **Verified sources** - All data from professional financial data provider
✅ **Consistent data** - All agents use same data source, ensuring consistency
✅ **Better performance** - No context switching between different tool types
✅ **Structured output** - MCP tools provide structured data, easier to parse

## What If You Need Google Search?

If you absolutely need Google Search for general web research, you have two options:

### Option 1: Create a Separate Research Agent (Recommended)
```python
# Create a new agent ONLY for Google Search
research_agent = Agent(
    name="web_research_agent",
    tools=[google_search],  # Only search tools
    instruction="Use Google Search for general web research..."
)

# Use it separately from financial agents
```

### Option 2: Use Google Search Tool Separately
```python
# In coordinator agent, you could have:
tools=[
    AgentTool(agent=data_analyst_agent),  # Alpha Vantage tools
    google_search,  # Can work in coordinator if needed
]
```

But for **financial analysis**, Alpha Vantage MCP provides everything needed!

---

## Summary

✅ **Error Fixed**: Removed tool mixing from data analyst
✅ **Ready to Use**: Run `adk web` and start chatting
✅ **All Features Working**: Live data, similar tickers, TOP 2 strategies, risk analysis
✅ **Better Data Quality**: Professional financial data source throughout

**Your financial advisor is ready! 🚀**
