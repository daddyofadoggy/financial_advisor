# Summary Agent and PDF Export Feature

## Overview

Added a new **Summary Agent** that generates an executive summary of the entire financial analysis and exports it as a downloadable PDF report. Also added **stock trend visualization** after the Data Analyst completes its analysis.

## New Features

### 1. Summary Agent (Lightweight Model)
- **Model:** `gemini-1.5-flash` (cost-effective, fast)
- **Purpose:** Synthesizes analysis from all 4 agents into a concise executive summary
- **Output:** Professional executive summary suitable for PDF export

### 2. Stock Trend Visualization
- **When:** After Data Analyst completes market analysis
- **What:** 30-day price trend chart showing stock performance
- **Format:** PNG image saved to Downloads folder

### 3. PDF Export
- **Library:** fpdf2 (simple, Pythonic PDF generation)
- **Content:** Complete financial analysis report with:
  - Market overview
  - Recommended strategies with return projections
  - Execution plan
  - Risk assessment
  - Final recommendations
  - Disclaimer
- **Output:** Professional PDF saved to Downloads folder

## New Components Created

### 1. Summary Agent
**Location:** `financial_advisor/sub_agents/summary_agent/`

**Files:**
- `__init__.py` - Package initialization
- `agent.py` - Summary agent using gemini-1.5-flash
- `prompt.py` - Comprehensive summarization instructions

**Key Features:**
- Synthesizes outputs from all previous agents
- Creates structured executive summary (3-5 pages)
- Includes all required disclaimers
- Optimized for PDF export format

### 2. Utilities
**Location:** `financial_advisor/utils/`

**Files:**
- `__init__.py` - Package exports
- `pdf_generator.py` - PDF report generation using fpdf2
- `stock_plotter.py` - Stock trend visualization using matplotlib

**`pdf_generator.py`:**
- Custom `FinancialReportPDF` class extending FPDF
- Automatic formatting (headers, footers, sections, tables)
- Professional layout with proper spacing
- Saves to Downloads folder with timestamped filename

**`stock_plotter.py`:**
- Parses market analysis for trend data
- Creates 30-day price trend chart
- Shows trend direction (uptrend/downtrend/sideways)
- Highlights current price
- Saves to Downloads folder

### 3. Visualization Tools
**Location:** `financial_advisor/tools/visualization_tools.py`

**Functions:**
- `create_stock_trend_plot(market_analysis: str) -> str`
- `export_summary_to_pdf(summary_text: str, ticker: str) -> str`

Both wrapped as `FunctionTool` for Google ADK compatibility.

## Updated Components

### 1. Coordinator Agent
**File:** `financial_advisor/agent.py`

**Changes:**
- Added `summary_agent` import and tool
- Added `create_stock_trend_plot` tool
- Added `export_summary_to_pdf` tool
- **Total tools:** 7 (4 agents + 3 function tools)

### 2. Coordinator Prompt
**File:** `financial_advisor/prompt.py`

**Changes:**
- **Step 1:** Data Analyst execution + stock trend visualization
- **Step 2:** Ask for Risk Attitude and Investment Period (AFTER plot)
- **Step 3-4:** Trading and Execution Analysts (unchanged)
- **Step 5:** Risk Analyst + summary request
- **Step 6:** Summary Agent + PDF export (optional)

### 3. Risk Analyst Prompt
**File:** `financial_advisor/sub_agents/risk_analyst/prompt.py`

**Changes:**
- Added section: "NEXT STEPS - EXECUTIVE SUMMARY GENERATION"
- Instructs agent to ask: "Would you like me to generate an executive summary and export it as a PDF?"
- Handles YES/NO responses
- If YES: Triggers summary_agent

## Workflow

### Complete User Journey

```
1. User provides ticker symbol (e.g., "AAPL")
   ↓
2. Data Analyst gathers market data
   ↓
3. 📊 Stock trend chart generated and saved
   ↓
4. User provides Risk Attitude & Investment Period
   ↓
5. Trading Analyst creates strategies
   ↓
6. Execution Analyst plans execution
   ↓
7. Risk Analyst evaluates risks
   ↓
8. Risk Analyst asks: "Want a summary PDF?"
   ↓
   ├─ YES → Summary Agent creates summary
   │         ↓
   │         PDF report generated and saved
   │         ↓
   │         User gets file path to download
   │
   └─ NO → Session concludes
```

### Tool Call Sequence (if user wants PDF)

1. `data_analyst_agent` → market_data_analysis_output
2. `create_stock_trend_plot(market_data_analysis_output)` → chart saved
3. `trading_analyst_agent` → proposed_trading_strategies_output
4. `execution_analyst_agent` → execution_plan_output
5. `risk_analyst_agent` → final_risk_assessment_output
6. `summary_agent` → executive_summary_output
7. `export_summary_to_pdf(executive_summary_output, ticker)` → PDF saved

## Dependencies Installed

```bash
uv pip install fpdf2 matplotlib
```

**Packages added:**
- `fpdf2==2.8.5` - PDF generation
- `matplotlib==3.10.7` - Plotting
- Supporting libraries: `pillow`, `fonttools`, `cycler`, `kiwisolver`, etc.

## File Structure

```
financial_advisor/
├── agent.py                          # ✅ Updated: Added summary_agent + tools
├── prompt.py                         # ✅ Updated: New workflow steps
├── sub_agents/
│   ├── data_analyst/                 # No changes
│   ├── trading_analyst/              # No changes
│   ├── execution_analyst/            # No changes
│   ├── risk_analyst/
│   │   ├── prompt.py                 # ✅ Updated: Ask for summary
│   └── summary_agent/                # ✨ NEW
│       ├── __init__.py
│       ├── agent.py                  # Gemini 1.5 Flash agent
│       └── prompt.py                 # Summarization instructions
├── tools/
│   ├── visualization_tools.py        # ✨ NEW: Plot & PDF tools
│   └── ...
└── utils/                            # ✨ NEW
    ├── __init__.py
    ├── pdf_generator.py              # PDF creation
    └── stock_plotter.py              # Chart creation
```

## State Keys

| Agent | Output State Key |
|-------|------------------|
| Data Analyst | `market_data_analysis_output` |
| Trading Analyst | `proposed_trading_strategies_output` |
| Execution Analyst | `execution_plan_output` |
| Risk Analyst | `final_risk_assessment_output` |
| **Summary Agent** | `executive_summary_output` |

## PDF Report Structure

```
═══════════════════════════════════════════════════════════
FINANCIAL ADVISORY EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════

REPORT DATE: [Date]
TICKER ANALYZED: [TICKER]
GENERATED BY: AI Financial Advisory System

───────────────────────────────────────────────────────────
1. MARKET OVERVIEW
───────────────────────────────────────────────────────────
- Current Market Position
- Market Sentiment
- Similar Investment Alternatives

───────────────────────────────────────────────────────────
2. RECOMMENDED STRATEGIES
───────────────────────────────────────────────────────────
- TOP STRATEGY #1 (with $1,000 projections)
- TOP STRATEGY #2 (with $1,000 projections)

───────────────────────────────────────────────────────────
3. EXECUTION PLAN
───────────────────────────────────────────────────────────
- Entry Strategy
- Risk Management
- Exit Strategy

───────────────────────────────────────────────────────────
4. RISK ASSESSMENT
───────────────────────────────────────────────────────────
- Comparative Risk Analysis (table)
- Key Risks to Monitor
- Risk-Adjusted Recommendation

───────────────────────────────────────────────────────────
5. FINAL RECOMMENDATIONS
───────────────────────────────────────────────────────────
- Recommended Action
- Key Decision Points
- Next Steps
- Critical Warnings

───────────────────────────────────────────────────────────
IMPORTANT DISCLAIMER
───────────────────────────────────────────────────────────
[Full legal disclaimer]

This entire process is for EDUCATIONAL and INFORMATIONAL
purposes ONLY and does NOT constitute financial advice.
All investment decisions should be made after conducting
your own thorough research and, ideally, consulting with
a qualified independent financial advisor.
═══════════════════════════════════════════════════════════
```

## Output File Naming

### Stock Trend Chart:
```
stock_trend_{TICKER}_{TIMESTAMP}.png
```
Example: `stock_trend_AAPL_20250120_143022.png`

### PDF Report:
```
financial_report_{TICKER}_{TIMESTAMP}.pdf
```
Example: `financial_report_AAPL_20250120_143045.pdf`

Both saved to: `~/Downloads/`

## Testing

```bash
# Test module loading
python -c "from financial_advisor.agent import root_agent; print('✅ Success')"

# Expected output:
# ✅ Success
# Root agent: financial_coordinator
# Number of tools: 7
```

**7 Tools:**
1. `data_analyst_agent` (AgentTool)
2. `create_stock_trend_plot` (FunctionTool)
3. `trading_analyst_agent` (AgentTool)
4. `execution_analyst_agent` (AgentTool)
5. `risk_analyst_agent` (AgentTool)
6. `summary_agent` (AgentTool)
7. `export_summary_to_pdf` (FunctionTool)

## How to Run

```bash
# Start the web interface
adk web

# Or specify the agent file
adk web financial_advisor/agent.py
```

## Usage Example

**User:** "Analyze AAPL stock"

**System:**
1. ✅ Data Analyst gathers market data
2. 📊 Stock trend chart saved to Downloads
3. ❓ Asks for Risk Attitude (e.g., "moderate")
4. ❓ Asks for Investment Period (e.g., "long-term")
5. ✅ Trading Analyst creates 5+ strategies, highlights TOP 2
6. ✅ Execution Analyst plans execution
7. ✅ Risk Analyst evaluates risks
8. ❓ Asks: "Want a summary PDF?"

**If YES:**
9. ✅ Summary Agent generates executive summary
10. 📄 PDF report saved to Downloads
11. ✅ User receives file path: `~/Downloads/financial_report_AAPL_20250120_143045.pdf`

## Benefits

### 1. Lightweight Model for Summarization
- **Cost:** Gemini 1.5 Flash is ~60% cheaper than Gemini 2.5 Pro
- **Speed:** Faster response time for summary generation
- **Efficiency:** Summary doesn't need the power of the pro model

### 2. Professional Output
- PDF export provides a professional deliverable
- Easy to share, print, or archive
- Structured format for easy reading

### 3. Visual Insights
- Stock trend chart provides quick visual understanding
- Shows trend direction at a glance
- Complements the textual analysis

### 4. User Control
- Optional summary generation (user can decline)
- Downloads saved locally (no upload needed)
- Clear file paths provided

### 5. Legal Protection
- Disclaimer prominently displayed in PDF
- Consistent messaging across all outputs
- Clear educational purpose stated

## API Call Optimization

**With Summary (worst case):**
- Data Analyst: ~10 calls
- Coordinator orchestration: ~2 calls
- Trading Analyst: ~2 calls
- Execution Analyst: ~2 calls
- Risk Analyst: ~2 calls
- **Summary Agent: ~2 calls**
- **Total: ~20 calls** (still under free tier limit with optimization)

**Without Summary:**
- Total: ~18 calls

**Tools (plotting, PDF):** No additional API calls - pure Python computation

## Disclaimers

The system now includes three levels of disclaimer:

1. **Initial disclaimer** (Coordinator greeting)
2. **Risk Analyst disclaimer** (End of risk analysis)
3. **PDF disclaimer** (Prominently in exported report)
4. **PDF export confirmation disclaimer** (After file saved)

All disclaimers emphasize:
- Educational and informational purposes ONLY
- NOT financial advice
- User should consult qualified financial advisor
- Google/Anthropic not liable

## Future Enhancements (Optional)

Potential improvements:
- [ ] Add more chart types (candlestick, volume, technical indicators)
- [ ] Support for multiple ticker comparison charts
- [ ] Email delivery of PDF report
- [ ] Customizable PDF templates
- [ ] HTML export option
- [ ] Interactive charts with Plotly

---

## Status

✅ **READY TO USE**

All features implemented and tested. You can now:

```bash
adk web
```

And enjoy the complete financial advisory experience with:
- Live market data
- Similar ticker recommendations
- TOP 2 strategy recommendations with $1,000 projections
- Strategy-wise risk analysis
- **Visual stock trend charts**
- **Executive summary PDF export**

**Remember:** This entire system is for EDUCATIONAL purposes ONLY!
