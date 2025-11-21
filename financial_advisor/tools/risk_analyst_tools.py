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

"""Risk Analyst tools - Volatility and risk metrics from Alpha Vantage MCP"""

from .alpha_vantage_tools import get_alpha_vantage_mcp_toolset


def get_risk_analyst_tools():
    """
    Get risk assessment tools for Risk Analyst

    Returns Alpha Vantage MCP toolset which includes:
    - ATR (Average True Range) - Volatility measurement
    - BBANDS (Bollinger Bands) - Volatility regime
    - STDDEV (Standard Deviation) - Price dispersion
    - Historical price data - Stress testing and drawdown analysis
    - Beta coefficient - Market sensitivity
    - Correlation analysis - Diversification assessment
    - And other risk metrics

    The MCP server provides all these tools automatically.
    """
    return get_alpha_vantage_mcp_toolset()
