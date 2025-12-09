# Financial Advisor AI: Advanced Risk Assessment & Strategy Platform

**Live Demo:** [https://financial-advisor-r4ixiexwla-ue.a.run.app/dev-ui/](https://financial-advisor-r4ixiexwla-ue.a.run.app/dev-ui/)

---

## Table of Contents

- [Overview](#overview)
- [Legal Disclaimer](#legal-disclaimer)
- [Agent Details](#agent-details)
- [Setup and Installation](#setup-and-installation)
- [Running the Agent](#running-the-agent)
- [Deployment](#deployment)

---

## Overview

**Financial Advisor AI** is a multi-agent system built with Google's Agent Development Kit (ADK) and powered by Gemini 2.5 Pro that orchestrates five specialized AI agents:Data Analyst (retrieving real-time market data via Alpha Vantage's Model Context Protocol with 60+ financial tools), Trading Analyst (developing investment strategies), Execution Analyst (creating actionable plans), Risk Analyst (evaluating potential risks), and Summary Agent (generating executive reports with PDF export)working sequentially through state-based communication to deliver comprehensive financial analysis and risk assessment for stock investments, all deployed on Google Cloud Run with an interactive web chat interface and RESTful APIs.

### Key Features

- **Multi-Agent Architecture**: Five specialized AI agents working in sequence
- **Real-Time Market Data**: Integration with Alpha Vantage via Model Context Protocol (MCP)
- **Comprehensive Analysis**: From data collection to risk assessment
- **Advanced Risk Assessment**: Dedicated agent for evaluating investment risks
- **Professional Reports**: Executive summaries with PDF export
- **Cloud-Native**: Deployed on Google Cloud Run with auto-scaling
- **Web Interface**: Interactive chat interface for easy access
- **RESTful APIs**: Programmatic access for integration

### Use Cases

- **Investment Firms**: Due diligence and risk assessment for stock picks
- **Financial Advisory**: Client portfolio analysis and recommendations
- **Corporate Finance**: Investment decision support for treasury operations
- **Individual Investors**: Personal investment strategy and risk evaluation
- **Trading Desks**: Quick analysis and risk evaluation

---

## Legal Disclaimer

### IMPORTANT: READ BEFORE USE

**THIS SOFTWARE IS PROVIDED FOR INFORMATIONAL AND EDUCATIONAL PURPOSES ONLY.**

#### No Financial Advice

The Financial Advisor AI system and its outputs do NOT constitute financial, investment, trading, or professional advice. The information provided by this system should NOT be used as the sole basis for making investment decisions.

#### User Acknowledgment

By using this software, you acknowledge and agree that:

1. **No Professional Relationship**: Use of this system does not create a financial advisor-client relationship.

2. **Educational Purpose**: This system is designed for educational and informational purposes to demonstrate multi-agent AI capabilities.

3. **Not a Substitute**: This system is NOT a substitute for professional financial advice from a licensed financial advisor, investment professional, or certified financial planner.

4. **Market Risks**: All investments carry risk. Past performance does not guarantee future results. You may lose some or all of your investment.

5. **Your Responsibility**: You are solely responsible for:
   - Conducting your own due diligence
   - Consulting with qualified financial professionals
   - Making your own investment decisions
   - Any financial losses incurred

6. **No Warranty**: This software is provided "AS IS" without warranties of any kind, express or implied, including but not limited to accuracy, completeness, or fitness for a particular purpose.

7. **Data Accuracy**: While we strive for accuracy, market data may be delayed, incomplete, or incorrect. Always verify information from official sources.

8. **Regulatory Compliance**: You are responsible for ensuring your use complies with all applicable laws and regulations in your jurisdiction.

#### Risk Disclosure

- Stock market investments involve substantial risk of loss
- AI-generated analysis may contain errors or biases
- Historical data does not predict future performance
- Market conditions can change rapidly
- Tax implications vary by jurisdiction and individual circumstances

#### Disclaimer of Liability

The creators, contributors, and operators of this software shall NOT be liable for any direct, indirect, incidental, consequential, or special damages arising from the use of this system, including but not limited to financial losses, lost profits, or investment decisions made based on system outputs.

**CONSULT A LICENSED FINANCIAL ADVISOR BEFORE MAKING INVESTMENT DECISIONS.**

---

## Agent Details

The Financial Advisor AI system consists of six specialized agents orchestrated through a coordinator:

### 1. Financial Coordinator (Root Agent)

**Role:** Orchestrates all sub-agents and manages the overall workflow

- **Model:** gemini-2.5-pro
- **Responsibilities:**
  - Receives user queries (stock tickers)
  - Invokes sub-agents in sequence via Agent-to-Agent (A2A) communication
  - Manages state-based data sharing between agents
  - Coordinates PDF export functionality
- **Tools:**
  - AgentTool for each sub-agent
  - export_summary_to_pdf function
- **Output Key:** financial_coordinator_output

---

### 2. Data Analyst Agent

**Role:** Retrieves and analyzes real-time market data

- **Model:** gemini-2.5-pro
- **Responsibilities:**
  - Fetches current stock quotes (price, volume, market cap)
  - Retrieves company fundamentals (P/E ratio, earnings, dividends)
  - Gathers market sentiment and news
  - Provides historical price data
- **Tools:**
  - Alpha Vantage MCP Toolset (60+ financial tools):
    - GLOBAL_QUOTE - Real-time stock quotes
    - COMPANY_OVERVIEW - Company fundamentals
    - TIME_SERIES_DAILY - Historical prices
    - NEWS_SENTIMENT - Market news and sentiment
    - Technical indicators (RSI, MACD, EMA, BBANDS, etc.)
- **Output Key:** market_data_analysis_output
- **External Integration:** Alpha Vantage API via Model Context Protocol (MCP)

---

### 3. Trading Analyst Agent

**Role:** Develops trading strategies based on market data

- **Model:** gemini-2.5-pro
- **Responsibilities:**
  - Analyzes market data from Data Analyst
  - Develops 5+ tailored trading strategies
  - Considers different investment styles (growth, value, momentum, etc.)
  - Provides strategy rationale and expected outcomes
- **Tools:** None (LLM-based reasoning)
- **Input:** Reads market_data_analysis_output from shared state
- **Output Key:** proposed_trading_strategies_output

---

### 4. Execution Analyst Agent

**Role:** Creates actionable execution plans for trading strategies

- **Model:** gemini-2.5-pro
- **Responsibilities:**
  - Reviews proposed trading strategies
  - Defines entry/exit points
  - Sets position sizing recommendations
  - Establishes stop-loss and take-profit levels
  - Creates timeline for execution
- **Tools:** None (LLM-based reasoning)
- **Input:** Reads proposed_trading_strategies_output from shared state
- **Output Key:** execution_plan_output

---

### 5. Risk Analyst Agent

**Role:** Evaluates and assesses investment risks

- **Model:** gemini-2.5-pro
- **Responsibilities:**
  - Analyzes all previous outputs (market data, strategies, execution plans)
  - Identifies potential risks (market, liquidity, company-specific)
  - Evaluates risk-reward ratios
  - Provides risk mitigation recommendations
  - Assigns risk ratings and scores
- **Tools:** None (LLM-based reasoning)
- **Input:** Reads all previous state outputs
- **Output Key:** final_risk_assessment_output

---

### 6. Summary Agent

**Role:** Generates executive summary and final report

- **Model:** gemini-2.5-pro
- **Responsibilities:**
  - Synthesizes all agent outputs into cohesive report
  - Creates executive summary
  - Highlights key findings and recommendations
  - Prepares content for PDF export
- **Tools:** None (LLM-based reasoning)
- **Input:** Reads all agent outputs from shared state
- **Output Key:** executive_summary_output

---

### Agent Communication Flow

```
User Input (Stock Ticker)
    |
    v
Financial Coordinator (Root Agent)
    |
    v [A2A - AgentTool]
Data Analyst --> [writes to state] --> market_data_analysis_output
    |
    v [reads state]
Trading Analyst --> [writes to state] --> proposed_trading_strategies_output
    |
    v [reads state]
Execution Analyst --> [writes to state] --> execution_plan_output
    |
    v [reads state]
Risk Analyst --> [writes to state] --> final_risk_assessment_output
    |
    v [reads state]
Summary Agent --> [writes to state] --> executive_summary_output
    |
    v
Financial Coordinator --> PDF Export + Chat Display
```

### State-Based Communication

All agents communicate through **shared state storage**:
- Each agent writes its output to a specific state key
- Subsequent agents read previous outputs from state
- Coordinator manages state access and orchestration
- Enables sequential processing with data persistence

---

## Setup and Installation

### Prerequisites

- **Python**: 3.11 or higher
- **Google Cloud Account**: For deployment (optional for local development)
- **Alpha Vantage API Key**: Get free key at https://www.alphavantage.co/support/#api-key
- **uv**: Python package manager (Installation: https://github.com/astral-sh/uv)

### Step 1: Clone the Repository

```bash
git clone https://github.com/daddyofadoggy/financial-advisor.git
cd financial-advisor
```

### Step 2: Install Dependencies

Using uv (recommended):

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv pip install -e .
```

Or using pip:

```bash
pip install -e .
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Google Cloud Configuration
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-east1
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name

# Alpha Vantage API Configuration
ALPHA_VANTAGE_API_KEY=your-api-key-here
ALPHA_VANTAGE_MCP_URL=https://mcp.alphavantage.co/mcp
```

**Important:**
- Never commit `.env` file to version control
- Get your free Alpha Vantage API key at: https://www.alphavantage.co/support/#api-key
- Free tier includes 25 requests/day, 5 requests/minute

### Step 4: Verify Installation

```bash
# Test that dependencies are installed
uv pip list

# Verify environment variables are loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('ALPHA_VANTAGE_API_KEY')[:10] + '...')"
```

---

## Running the Agent

### Option 1: Terminal Chat Interface (Quick Start)

Run the agent in your terminal with an interactive chat:

```bash
uv run adk run .
```

**Usage:**
```
> Enter your query: AAPL
[Agent processes and returns analysis]

> Enter your query: Tell me about Microsoft stock
[Agent processes MSFT analysis]

> Enter your query: exit
```

### Option 2: Web Interface (Recommended)

Launch a full web UI with chat interface:

```bash
uv run adk web .
```

Then open your browser to: **http://localhost:8000**

**Features:**
- Interactive chat interface
- Session management
- Conversation history
- PDF report download
- Real-time agent responses

### Option 3: Python Script

Use the agent programmatically:

```python
from google.adk import App
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from financial_advisor.agent import root_agent

# Create ADK App
app = App(name="financial_advisor", root_agent=root_agent)
session_service = InMemorySessionService()
runner = Runner(app=app, session_service=session_service)

# Run query
result = await runner.run_async(
    user_content="Analyze AAPL stock",
    session_id="my_session"
)

print(result.get("financial_coordinator_output"))
```

### Example Queries

Try these queries with your agent:

```
AAPL
GOOGL
TSLA
Analyze Microsoft stock
What's the risk profile of NVDA?
Tell me about Amazon's trading strategies
```

### Expected Output

The agent will provide:

1. **Market Data Analysis**: Current price, volume, market cap, fundamentals
2. **Trading Strategies**: 5+ strategies (growth, value, momentum, etc.)
3. **Execution Plan**: Entry/exit points, position sizing, stop-loss levels
4. **Risk Assessment**: Risk evaluation, mitigation strategies, risk rating
5. **Executive Summary**: Comprehensive report with key findings
6. **PDF Export**: Downloadable professional report (via web interface)

---

## Deployment

### Deploy to Google Cloud Run

#### Prerequisites

- Google Cloud Account with billing enabled
- gcloud CLI installed and configured
- Docker (optional, Cloud Build handles this)

#### Quick Deploy

```bash
# Make deployment script executable
chmod +x deployment/deploy_cloud_run.sh

# Deploy to Cloud Run
./deployment/deploy_cloud_run.sh
```

#### What the Script Does

1. **Enables Required APIs**:
   - Cloud Build API
   - Cloud Run API
   - Artifact Registry API

2. **Builds Container**:
   - Uses Cloud Build to create Docker image
   - Installs all dependencies via uv
   - Configures for port 8080

3. **Deploys to Cloud Run**:
   - Region: us-east1 (configurable)
   - Memory: 2Gi
   - CPU: 2 cores
   - Timeout: 300 seconds
   - Auto-scaling: 0-10 instances
   - Public access enabled

4. **Sets Environment Variables**:
   - ALPHA_VANTAGE_API_KEY: Your API key
   - GOOGLE_GENAI_USE_VERTEXAI=1

#### Manual Deployment

```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build container image
gcloud builds submit --tag gcr.io/${PROJECT_ID}/financial-advisor

# Deploy to Cloud Run
gcloud run deploy financial-advisor \
  --image=gcr.io/${PROJECT_ID}/financial-advisor \
  --platform=managed \
  --region=us-east1 \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --timeout=300 \
  --min-instances=0 \
  --max-instances=10 \
  --set-env-vars="ALPHA_VANTAGE_API_KEY=your-key" \
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=1"
```

#### Access Your Deployment

After deployment, you'll receive a URL like:
```
https://financial-advisor-xxxxxxxxxx-ue.a.run.app
```

**Endpoints:**
- **Web Chat**: /dev-ui/
- **API Docs**: /docs
- **Health Check**: /health

#### Update Deployment

To deploy changes:

```bash
# After making code changes
./deployment/deploy_cloud_run.sh
```

To update only environment variables:

```bash
gcloud run services update financial-advisor \
  --region=us-east1 \
  --set-env-vars="ALPHA_VANTAGE_API_KEY=new-key"
```

#### Monitoring

```bash
# View service details
gcloud run services describe financial-advisor --region=us-east1

# View logs
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=financial-advisor" \
  --limit=50

# View in Cloud Console
open https://console.cloud.google.com/run
```

#### Cost Estimates

Cloud Run pricing (us-east1):
- **Idle**: $0/month (scales to zero)
- **Light usage** (100 requests/day): $5-10/month
- **Moderate usage** (1,000 requests/day): $30-50/month

Plus:
- Gemini 2.5 Pro API: Pay-per-token
- Alpha Vantage API: Free tier (25 requests/day)

---

## Project Structure

```
financial-advisor/
├── financial_advisor/
│   ├── agent.py                    # Root coordinator agent
│   ├── prompt.py                   # Main orchestration logic
│   ├── fast_api_app.py            # FastAPI wrapper (optional)
│   ├── sub_agents/
│   │   ├── data_analyst/
│   │   │   ├── agent.py           # Data gathering agent
│   │   │   └── prompt.py          # Data collection instructions
│   │   ├── trading_analyst/       # Strategy generation
│   │   ├── execution_analyst/     # Action planning
│   │   ├── risk_analyst/          # Risk assessment
│   │   └── summary_agent/         # Report generation
│   ├── tools/
│   │   ├── alpha_vantage_tools.py # MCP toolset configuration
│   │   ├── visualization_tools.py # PDF export
│   │   └── __init__.py
│   └── utils/
│       └── pdf_generator.py       # PDF creation utilities
├── deployment/
│   └── deploy_cloud_run.sh        # Cloud Run deployment script
├── Dockerfile                      # Container definition
├── pyproject.toml                  # Python dependencies
├── .env                            # Environment variables (not in git)
├── README.md                       # This file
└── deployment_steps.md             # Detailed deployment guide
```


---

## Architecture

### Technology Stack

**User Interface Layer**
- ADK Web UI (Chat Interface)
- FastAPI (API Documentation)

**Application Layer (Cloud Run)**
- ADK Framework (Agent Orchestration)
- Python 3.11
- Uvicorn (ASGI Server)

**Agent Layer (ADK)**
- Financial Coordinator
- 5 Specialized Sub-Agents
- State-Based Communication

**Tools & Services Layer**
- Alpha Vantage MCP (Market Data)
- Gemini 2.5 Pro (LLM)
- PDF Generator (Reports)

**Infrastructure Layer (GCP)**
- Cloud Run (Serverless Container)
- Cloud Build (CI/CD)
- Container Registry (Image Storage)
- Cloud Logging (Monitoring)

---

## Additional Resources

### Documentation

- **ADK Documentation**: https://cloud.google.com/agent-development-kit
- **Cloud Run Documentation**: https://cloud.google.com/run/docs
- **Alpha Vantage API**: https://www.alphavantage.co/documentation/
- **Gemini API**: https://ai.google.dev/docs

### Monitoring & Support

- **Live Demo**: https://financial-advisor-r4ixiexwla-ue.a.run.app/dev-ui/
- **API Documentation**: https://financial-advisor-r4ixiexwla-ue.a.run.app/docs
- **Cloud Console**: https://console.cloud.google.com/run
- **GitHub Issues**: https://github.com/yourusername/financial-advisor/issues

---
FINANCIAL ADVISORY EXECUTIVE SUMMARY ═══════════════════════════════════════════════════════════════════════════

REPORT DATE: 2024-10-27 TICKER ANALYZED: AAPL GENERATED BY: AI Financial Advisory System

═══════════════════════════════════════════════════════════════════════════ 1. MARKET OVERVIEW ═══════════════════════════════════════════════════════════════════════════

Current Market Position:

Current Stock Price: $277.89
Price Change: -$0.89 (-0.32%)
52-Week Range: $168.63 - $288.62
Market Cap: $4.14 Trillion
P/E Ratio: 37.32
Sector: TECHNOLOGY
Market Sentiment:

Overall Sentiment: Cautiously Bullish
Key Themes:
The stock is trading at a premium valuation (high P/E ratio), reflecting strong investor confidence in future growth.
Apple maintains its dominant position as a market leader in the technology sector with robust fundamentals.
While near its 52-week high, the stock shows slight negative short-term momentum, suggesting a potential consolidation phase.
═══════════════════════════════════════════════════════════════════════════ 2. RECOMMENDED STRATEGIES ═══════════════════════════════════════════════════════════════════════════

TOP STRATEGY #1: Sector Leader Momentum

Description: This strategy aims to capitalize on AAPL's strong uptrend and market leadership by entering on controlled pullbacks or confirmed breakouts.
Risk Level: Medium
TOP STRATEGY #2: Value-Oriented Entry Strategy

Description: This patient strategy focuses on acquiring AAPL shares at a more favorable valuation, waiting for a market-driven price correction of 10-15%.
Risk Level: Low-to-Medium
═══════════════════════════════════════════════════════════════════════════ 3. EXECUTION PLAN ═══════════════════════════════════════════════════════════════════════════

Entry Strategy: Use Limit Orders for value entries and Stop-Limit Orders for breakout entries. Risk no more than 1% of total portfolio value on a single trade.
Risk Management: Move stop-loss to breakeven after a 1:1 risk-reward gain. Use a trailing stop to lock in profits on a long-term hold.
Profit-Taking: Consider selling partial positions at pre-defined profit targets (e.g., 2x or 3x the initial risk) to de-risk the trade.
═══════════════════════════════════════════════════════════════════════════ 4. RISK ASSESSMENT ═══════════════════════════════════════════════════════════════════════════

Comparative Risk Analysis: Strategy #1 (Momentum) carries higher volatility and market risk, while Strategy #2 (Value-Entry) has lower market risk but higher opportunity cost risk (cash drag).

Key Risks to Monitor:

Valuation Risk: AAPL's high P/E ratio makes it vulnerable to a correction.
Opportunity Cost: The value strategy risks missing gains if the stock doesn't pull back.
Momentum Reversal: The momentum strategy is vulnerable to a market downturn.
Risk-Adjusted Recommendation: Strategy #2 (Value-Oriented Entry) is recommended as it aligns better with a moderate risk profile, prioritizing capital preservation.

═══════════════════════════════════════════════════════════════════════════ 5. FINAL RECOMMENDATIONS ═══════════════════════════════════════════════════════════════════════════

Recommended Action: Proceed with a hybrid approach:

Initial Allocation: Deploy 25-30% of your intended capital into AAPL now, using a Dollar-Cost Averaging (DCA) approach over the next 3 months.
Set Value-Entry Orders: Place Good 'Til Canceled (GTC) Limit Orders for the remaining 70-75% of capital at tiered levels corresponding to a 10% and 15% correction from the peak.
This entire process is for EDUCATIONAL and INFORMATIONAL purposes ONLY and does NOT constitute financial advice. All investment decisions should be made after conducting your own thorough research and, ideally, consulting with a qualified independent financial advisor.

---
## License

Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

**Remember**: This is an educational tool. Always consult licensed financial professionals before making investment decisions.
