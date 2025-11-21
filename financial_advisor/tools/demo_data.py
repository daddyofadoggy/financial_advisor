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

"""Demo data for testing without API calls"""

DEMO_MARKET_DATA = {
    "AAPL": {
        "symbol": "AAPL",
        "current_price": 185.50,
        "change": 2.75,
        "change_percent": 1.51,
        "volume": 52_450_000,
        "previous_close": 182.75,
        "market_cap": 2_850_000_000_000,
        "pe_ratio": 29.5,
        "eps": 6.29,
        "week_52_high": 199.62,
        "week_52_low": 164.08,
        "dividend_yield": 0.50,
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."
    },
    "MSFT": {
        "symbol": "MSFT",
        "current_price": 425.50,
        "change": 5.25,
        "change_percent": 1.25,
        "volume": 24_550_000,
        "previous_close": 420.25,
        "market_cap": 3_160_000_000_000,
        "pe_ratio": 35.8,
        "eps": 11.89,
        "week_52_high": 468.35,
        "week_52_low": 362.90,
        "dividend_yield": 0.75,
        "sector": "Technology",
        "industry": "Software—Infrastructure",
        "description": "Microsoft Corporation develops and supports software, services, devices, and solutions worldwide."
    },
    "GOOGL": {
        "symbol": "GOOGL",
        "current_price": 142.30,
        "change": -0.85,
        "change_percent": -0.59,
        "volume": 28_150_000,
        "previous_close": 143.15,
        "market_cap": 1_780_000_000_000,
        "pe_ratio": 25.4,
        "eps": 5.61,
        "week_52_high": 155.08,
        "week_52_low": 121.46,
        "dividend_yield": 0.00,
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "description": "Alphabet Inc. offers various products and platforms in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America."
    },
    "AMZN": {
        "symbol": "AMZN",
        "current_price": 178.25,
        "change": 3.50,
        "change_percent": 2.00,
        "volume": 45_200_000,
        "previous_close": 174.75,
        "market_cap": 1_850_000_000_000,
        "pe_ratio": 45.2,
        "eps": 3.94,
        "week_52_high": 201.20,
        "week_52_low": 139.52,
        "dividend_yield": 0.00,
        "sector": "Consumer Cyclical",
        "industry": "Internet Retail",
        "description": "Amazon.com, Inc. engages in the retail sale of consumer products and subscriptions in North America and internationally."
    },
    "TSLA": {
        "symbol": "TSLA",
        "current_price": 242.80,
        "change": -4.20,
        "change_percent": -1.70,
        "volume": 95_400_000,
        "previous_close": 247.00,
        "market_cap": 775_000_000_000,
        "pe_ratio": 68.5,
        "eps": 3.54,
        "week_52_high": 299.29,
        "week_52_low": 152.37,
        "dividend_yield": 0.00,
        "sector": "Consumer Cyclical",
        "industry": "Auto Manufacturers",
        "description": "Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems."
    }
}


def get_demo_market_analysis(ticker: str) -> str:
    """
    Generate a demo market analysis report without making API calls

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")

    Returns:
        str: Formatted market analysis report
    """
    ticker = ticker.upper()

    if ticker not in DEMO_MARKET_DATA:
        # Return analysis for AAPL as default
        ticker = "AAPL"
        note = f"\n**Note:** Demo data for {ticker} not available. Showing AAPL as example.\n"
    else:
        note = "\n**Note:** This is DEMO DATA for testing purposes. Not real-time market data.\n"

    data = DEMO_MARKET_DATA[ticker]

    report = f"""
Market Analysis Report for: {data['symbol']} (DEMO MODE)
{note}
Report Date: 2025-01-20
Information Source: Demo data for testing purposes

**1. Current Market Data:**
   * **Current Stock Price:** ${data['current_price']:.2f}
   * **Price Change:** ${data['change']:+.2f} ({data['change_percent']:+.2f}%)
   * **Trading Volume:** {data['volume']:,}
   * **Previous Close:** ${data['previous_close']:.2f}

**2. Company Fundamentals:**
   * **Market Capitalization:** ${data['market_cap']/1_000_000_000:.2f}B
   * **52-Week Range:** ${data['week_52_low']:.2f} - ${data['week_52_high']:.2f}
   * **P/E Ratio:** {data['pe_ratio']:.1f}
   * **EPS:** ${data['eps']:.2f}
   * **Dividend Yield:** {data['dividend_yield']:.2f}%
   * **Sector:** {data['sector']}
   * **Industry:** {data['industry']}
   * **Company Description:** {data['description']}

**3. Executive Summary:**
   * {data['symbol']} showing {'positive' if data['change'] > 0 else 'negative'} momentum with {data['change_percent']:+.2f}% change
   * Trading at P/E of {data['pe_ratio']:.1f}, {'above' if data['pe_ratio'] > 30 else 'below'} market average
   * {'Strong' if data['market_cap'] > 1_000_000_000_000 else 'Moderate'} fundamentals with ${data['market_cap']/1_000_000_000:.0f}B market cap
   * Currently trading at {'near high' if data['current_price'] > (data['week_52_high'] * 0.9) else 'mid-range' if data['current_price'] > (data['week_52_low'] * 1.3) else 'near low'} of 52-week range
   * {'No dividend' if data['dividend_yield'] == 0 else f"Dividend yield of {data['dividend_yield']:.2f}% indicates shareholder returns"}

**IMPORTANT:** This is demo data for testing the system without using API calls.
For real-time market data, ensure your Alpha Vantage API quota is available.
"""

    return report.strip()
