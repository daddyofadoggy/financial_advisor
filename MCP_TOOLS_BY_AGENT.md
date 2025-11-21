# MCP Tools Distribution Across All Agents

## Overview

All agents in the financial-advisor system now leverage specialized MCP (Model Context Protocol) tools from the Alpha Vantage MCP server. Each agent has access to domain-specific tools optimized for their particular responsibilities.

**Total Tools Integrated: 26**
- Data Analyst: 6 tools
- Trading Analyst: 7 tools
- Execution Analyst: 6 tools
- Risk Analyst: 7 tools

---

## Agent-by-Agent Tool Breakdown

### 1. Data Analyst Agent (6 Tools)

**Purpose:** Market research, live data collection, similar ticker recommendations

| Tool Name | Purpose | Key Output |
|-----------|---------|------------|
| `alpha_vantage_global_quote` | Real-time stock price | Current price, change, volume, prev close |
| `alpha_vantage_company_overview` | Company fundamentals | Market cap, P/E, EPS, sector, industry, dividend |
| `alpha_vantage_time_series_daily` | Historical price data | OHLCV data for 30-day trend analysis |
| `alpha_vantage_symbol_search` | Find similar tickers | Ticker symbols and company names |
| `alpha_vantage_news_sentiment` | News with sentiment analysis | Articles with bullish/bearish/neutral scores |
| `alpha_vantage_sma` | Simple Moving Average | Trend indicator for basic analysis |

**Additional Tool:**
- `google_search` - Supplementary research for SEC filings and analyst opinions

**Use Cases:**
- Fetch live stock price for target ticker
- Find 3 similar stocks by price range (±30%) and sector
- Analyze news sentiment to gauge market mood
- Provide comprehensive market context for strategy formulation

---

### 2. Trading Analyst Agent (7 Tools) ⭐ NEW

**Purpose:** Strategy formulation with technical analysis, identifying top 2 strategies

| Tool Name | Indicator Type | Strategy Application |
|-----------|---------------|---------------------|
| `alpha_vantage_rsi` | Momentum | Overbought/oversold conditions (>70 / <30) |
| `alpha_vantage_macd` | Trend + Momentum | Trend following, crossover signals |
| `alpha_vantage_ema` | Trend | Moving average crossovers, support/resistance |
| `alpha_vantage_bbands` | Volatility | Mean reversion, breakout identification |
| `alpha_vantage_stoch` | Momentum | Overbought/oversold confirmation, divergence |
| `alpha_vantage_adx` | Trend Strength | Filter strong trends (ADX > 25) |
| `alpha_vantage_obv` | Volume | Volume trend confirmation, price-volume divergence |

**Use Cases:**
- **Momentum Strategy:** Use RSI + MACD to identify overbought/oversold with momentum confirmation
  - Entry: RSI < 30 AND MACD crosses above signal line
  - Exit: RSI > 70 OR MACD crosses below signal line

- **Mean Reversion Strategy:** Use Bollinger Bands + Stochastic
  - Entry: Price touches lower Bollinger Band AND Stochastic < 20
  - Exit: Price returns to middle band OR Stochastic > 80

- **Trend Following Strategy:** Use EMA + ADX + OBV
  - Entry: Price above 50-day EMA AND ADX > 25 AND OBV rising
  - Exit: Price crosses below 50-day EMA OR ADX < 20

- **Breakout Strategy:** Use Bollinger Bands squeeze + ADX
  - Entry: Bands narrow (low volatility) then price breaks out with volume
  - Exit: ADX peaks and starts declining

**Expected Benefits:**
- More precise entry/exit conditions based on real data
- Better expected return estimates using historical indicator performance
- Quantifiable strategy parameters instead of subjective descriptions
- Ability to backtest strategy logic using historical indicator values

---

### 3. Execution Analyst Agent (6 Tools) ⭐ NEW

**Purpose:** Optimal order execution, liquidity analysis, slippage estimation

| Tool Name | Purpose | Execution Application |
|-----------|---------|----------------------|
| `alpha_vantage_time_series_intraday` | Intraday price patterns | Identify optimal execution times (e.g., avoid market open volatility) |
| `alpha_vantage_quote_endpoint` | Real-time bid-ask spread | Estimate slippage costs for limit vs market orders |
| `alpha_vantage_vwap` | Volume Weighted Avg Price | Benchmark execution quality, target price for large orders |
| `alpha_vantage_obv_execution` | On-Balance Volume | Assess current liquidity trends |
| `alpha_vantage_adv` | Average Daily Volume | Determine if stock can handle $1,000 position without impact |
| `alpha_vantage_market_status` | Market open/close | Time order execution appropriately |

**Use Cases:**
- **Liquidity Assessment:**
  - Check Average Daily Volume (ADV) for the ticker
  - For $1,000 position, ensure it's < 1% of ADV to minimize market impact
  - Use OBV to confirm volume is sufficient for smooth execution

- **Slippage Estimation:**
  - Get current bid-ask spread from quote endpoint
  - For market orders: Estimate slippage = spread / 2
  - For limit orders: Estimate fill probability based on order book depth

- **Timing Optimization:**
  - Analyze intraday patterns to identify low-volatility windows
  - Avoid first/last 30 minutes of trading (high volatility)
  - Use VWAP as target price for large orders throughout the day

- **Order Type Selection:**
  - Narrow spread (<0.1%) → Market orders acceptable
  - Wide spread (>0.5%) → Use limit orders to reduce costs
  - High volume (ADV > $10M) → Can execute quickly
  - Low volume (ADV < $1M) → Break order into smaller chunks

**Expected Benefits:**
- Reduce execution costs by 0.1-0.5% through optimal timing
- Better order type selection based on real liquidity data
- Realistic execution plans tailored to actual market conditions
- Position sizing appropriate for stock's liquidity profile

---

### 4. Risk Analyst Agent (7 Tools) ⭐ NEW

**Purpose:** Volatility assessment, risk quantification, stress testing

| Tool Name | Risk Metric | Risk Application |
|-----------|-------------|------------------|
| `alpha_vantage_atr` | Average True Range | Position sizing, stop-loss placement based on volatility |
| `alpha_vantage_bbands_volatility` | Bollinger Bands Width | Volatility regime identification (expanding/contracting) |
| `alpha_vantage_stddev` | Standard Deviation | Price dispersion, drawdown estimation |
| `alpha_vantage_time_series_historical` | Full historical data | Stress testing, maximum historical drawdown |
| `alpha_vantage_vix` | Volatility Index (VIX) | Market-wide fear gauge, correlation risk |
| `alpha_vantage_correlation` | Stock correlation | Diversification analysis, portfolio risk |
| `alpha_vantage_beta` | Beta coefficient | Systematic risk, market sensitivity |

**Use Cases:**
- **Volatility-Based Position Sizing:**
  - Calculate ATR for the stock
  - Position size = Risk per trade / (2 × ATR)
  - Example: $100 risk, ATR = $2 → Position = $100 / $4 = 25 shares

- **Stop-Loss Placement:**
  - Use ATR for volatility-adjusted stops
  - Conservative: Stop at entry - (3 × ATR)
  - Aggressive: Stop at entry - (1.5 × ATR)
  - Prevents getting stopped out by normal price fluctuations

- **Maximum Drawdown Analysis:**
  - Get full historical data (20+ years if available)
  - Calculate peak-to-trough declines
  - Estimate: "Based on history, strategy could face [X]% drawdown"
  - For $1,000 investment: "Potential max loss of $[X × 10]"

- **Stress Testing Scenarios:**
  - Identify worst historical periods (2008 crisis, COVID crash)
  - Simulate strategy performance during those periods
  - Provide realistic worst-case scenarios for user

- **Correlation Risk Assessment:**
  - If user holds other stocks, check correlation
  - High correlation (>0.7) = portfolio concentration risk
  - Recommend diversification into low/negative correlated assets

- **Market Risk (Beta Analysis):**
  - Beta > 1: Stock amplifies market moves (higher risk)
  - Beta < 1: Stock dampens market moves (lower risk)
  - Beta = 1.5 means 50% more volatile than market
  - Adjust risk assessment based on user's market outlook

**Expected Benefits:**
- Quantitative risk metrics instead of qualitative descriptions
- Realistic maximum drawdown estimates from historical data
- Position sizing recommendations based on actual volatility
- Strategy-specific risk scores (1-10) based on measured volatility
- Better alignment assessment with user risk tolerance

---

## Tool Usage by Agent: Summary Matrix

```
┌──────────────────────┬─────────────┬─────────────────┬──────────────────┬──────────────┐
│ Tool Category        │ Data        │ Trading         │ Execution        │ Risk         │
│                      │ Analyst     │ Analyst         │ Analyst          │ Analyst      │
├──────────────────────┼─────────────┼─────────────────┼──────────────────┼──────────────┤
│ Market Data          │ ✓✓✓         │                 │                  │              │
│ (price, company info)│ 3 tools     │                 │                  │              │
├──────────────────────┼─────────────┼─────────────────┼──────────────────┼──────────────┤
│ Technical Indicators │ ✓           │ ✓✓✓✓✓✓✓         │                  │              │
│ (RSI, MACD, EMA...)  │ 1 tool (SMA)│ 7 tools         │                  │              │
├──────────────────────┼─────────────┼─────────────────┼──────────────────┼──────────────┤
│ Liquidity/Execution  │             │                 │ ✓✓✓✓✓✓           │              │
│ (volume, spread...)  │             │                 │ 6 tools          │              │
├──────────────────────┼─────────────┼─────────────────┼──────────────────┼──────────────┤
│ Volatility/Risk      │             │                 │                  │ ✓✓✓✓✓✓✓      │
│ (ATR, stddev, beta...│             │                 │                  │ 7 tools      │
├──────────────────────┼─────────────┼─────────────────┼──────────────────┼──────────────┤
│ News & Sentiment     │ ✓           │                 │                  │              │
│                      │ 1 tool      │                 │                  │              │
├──────────────────────┼─────────────┼─────────────────┼──────────────────┼──────────────┤
│ Search & Discovery   │ ✓           │                 │                  │              │
│ (similar tickers...) │ 1 tool      │                 │                  │              │
├──────────────────────┼─────────────┼─────────────────┼──────────────────┼──────────────┤
│ External Search      │ Google      │                 │                  │              │
│                      │ Search      │                 │                  │              │
├──────────────────────┼─────────────┼─────────────────┼──────────────────┼──────────────┤
│ TOTAL TOOLS          │ 6 + search  │ 7               │ 6                │ 7            │
└──────────────────────┴─────────────┴─────────────────┴──────────────────┴──────────────┘
```

---

## Benefits of Multi-Agent Tool Distribution

### 1. **Specialized Expertise**
- Each agent has tools tailored to their specific domain
- No tool overlap/confusion - clear responsibility boundaries
- Agents become true domain experts with appropriate capabilities

### 2. **Better Collaboration**
- Data Analyst provides raw data → Trading Analyst adds technical analysis
- Trading Analyst defines strategies → Execution Analyst optimizes execution
- Execution Analyst plans orders → Risk Analyst quantifies risks
- Each layer adds value using specialized tools

### 3. **Quantitative vs Qualitative**

**Before (qualitative):**
- "This is a high-risk strategy" ❌
- "Entry when momentum is strong" ❌
- "Stock is fairly liquid" ❌

**After (quantitative with tools):**
- "Beta of 1.8 and ATR of $3 indicates high volatility; expected max drawdown: 25%" ✅
- "Entry when RSI crosses below 30 AND MACD histogram turns positive" ✅
- "Average daily volume of $50M; $1,000 order represents 0.002% - excellent liquidity" ✅

### 4. **Improved Accuracy**
- Expected returns based on historical indicator performance
- Risk metrics calculated from actual volatility data
- Execution costs estimated from real bid-ask spreads
- Everything grounded in real market data, not assumptions

### 5. **User Confidence**
- Users see concrete numbers, not vague descriptions
- Strategies backed by technical analysis with clear signals
- Risk assessments include historical worst-case scenarios
- Execution plans based on actual liquidity conditions

---

## Example: Complete Workflow with Tools

### User Request: "Analyze AAPL for moderate risk, long-term investment with $1,000"

**Step 1: Data Analyst**
```
Tools Used:
- alpha_vantage_global_quote(symbol="AAPL")
  → Price: $180.50, Volume: 50M, Change: +2.5%
- alpha_vantage_company_overview(symbol="AAPL")
  → Market Cap: $2.8T, P/E: 29.5, Sector: Technology
- alpha_vantage_symbol_search + global_quote for similar stocks
  → Found: MSFT ($375), GOOGL ($140), META ($485)
  → Selected 3 within ±30% of AAPL price
- alpha_vantage_news_sentiment(tickers="AAPL")
  → Sentiment: Moderately Bullish (score: 0.35)

Output: Comprehensive market report with live data + 3 similar tickers
```

**Step 2: Trading Analyst**
```
Tools Used:
- alpha_vantage_rsi(symbol="AAPL", interval="daily")
  → RSI: 58 (neutral, slightly bullish)
- alpha_vantage_macd(symbol="AAPL", interval="daily")
  → MACD above signal line (bullish trend)
- alpha_vantage_ema(symbol="AAPL", time_period=50)
  → Price $180.50 above 50-day EMA of $175 (uptrend)
- alpha_vantage_adx(symbol="AAPL", interval="daily")
  → ADX: 28 (strong trend)
- alpha_vantage_bbands(symbol="AAPL", interval="daily")
  → Price at middle band (neutral)

Strategies Developed:
1. Trend Following (EMA crossover) - Expected Return: 12-18%
2. Momentum Breakout (RSI + MACD) - Expected Return: 15-25% ← TOP #1
3. Dividend Growth (buy-and-hold) - Expected Return: 10-15%
4. Mean Reversion (Bollinger Bands) - Expected Return: 8-14%
5. Volume Confirmation (OBV) - Expected Return: 13-20% ← TOP #2

TOP 2 Selected with $1,000 projections:
- Strategy #1: Momentum Breakout
  - Conservative: 10% → $1,100
  - Moderate: 20% → $1,200
  - Aggressive: 30% → $1,300
- Strategy #2: Volume Confirmation
  - Conservative: 8% → $1,080
  - Moderate: 16% → $1,160
  - Aggressive: 24% → $1,240
```

**Step 3: Execution Analyst**
```
Tools Used:
- alpha_vantage_quote_endpoint(symbol="AAPL")
  → Bid: $180.48, Ask: $180.52, Spread: $0.04 (0.02%)
- alpha_vantage_adv(symbol="AAPL", period=30)
  → Average Daily Volume: $9 billion
- alpha_vantage_time_series_intraday(symbol="AAPL", interval="5min")
  → Best execution time: 10:30-11:00 AM (lowest volatility)
- alpha_vantage_vwap(symbol="AAPL", interval="15min")
  → VWAP: $180.45 (current price slightly above)
- alpha_vantage_market_status()
  → Market open, normal trading hours

Execution Plan:
- Order Type: Limit order (spread is narrow but save $0.02/share)
- Position Size: 5-6 shares for $1,000
- Timing: Place order during 10:30-11:00 AM window
- Limit Price: $180.45 (VWAP target)
- Expected Slippage: $0.01-0.02 per share (minimal)
- Estimated Fill Probability: 95% (excellent liquidity)
```

**Step 4: Risk Analyst**
```
Tools Used:
- alpha_vantage_atr(symbol="AAPL", interval="daily")
  → ATR: $2.50 (daily volatility)
- alpha_vantage_stddev(symbol="AAPL", time_period=30)
  → Std Dev: $3.20 (30-day)
- alpha_vantage_time_series_historical(symbol="AAPL", outputsize="full")
  → Max historical drawdown: -32% (COVID crash 2020)
- alpha_vantage_beta(symbol="AAPL")
  → Beta: 1.25 (25% more volatile than market)
- alpha_vantage_bbands_volatility(symbol="AAPL")
  → Band width: Medium (normal volatility regime)
- alpha_vantage_vix()
  → VIX: 15 (low market fear)

Risk Analysis - Strategy #1 (Momentum Breakout):
- Volatility Risk: MEDIUM (ATR $2.50, daily swings ±1.4%)
- Max Drawdown Risk: 25-30% ($250-300 loss on $1,000)
- Stop-Loss Recommendation: $180.50 - (2 × $2.50) = $175.50
- Position Size: 5 shares × $180.50 = $902.50 (safe for $1,000)
- Overall Risk Score: 6/10 (moderate-high)

Risk Analysis - Strategy #2 (Volume Confirmation):
- Volatility Risk: MEDIUM-LOW (same ATR but longer hold)
- Max Drawdown Risk: 20-25% ($200-250 loss on $1,000)
- Stop-Loss Recommendation: $175.00 (technical support)
- Overall Risk Score: 5/10 (moderate)

Recommendation: Strategy #2 better matches "moderate risk" profile
```

---

## Summary

### Tool Distribution Philosophy

1. **Data Analyst = Data Gatherer**
   - Fetches raw market data
   - No analysis, just collection
   - Tools: Market data + search

2. **Trading Analyst = Strategy Designer**
   - Analyzes data with technical indicators
   - Formulates strategies with precise entry/exit rules
   - Tools: Technical indicators

3. **Execution Analyst = Implementation Planner**
   - Determines HOW to execute the strategy
   - Optimizes for cost and timing
   - Tools: Liquidity + execution analysis

4. **Risk Analyst = Risk Quantifier**
   - Measures volatility and risk
   - Provides worst-case scenarios
   - Tools: Volatility + risk metrics

### Key Advantages

✅ **26 specialized tools** across 4 agents
✅ **No tool overlap** - clear responsibilities
✅ **Quantitative outputs** instead of qualitative guesses
✅ **Real market data** backing every recommendation
✅ **Better collaboration** - each agent adds unique value

**Result:** A truly professional financial advisory system where every recommendation is backed by real-time market data and quantitative analysis.
