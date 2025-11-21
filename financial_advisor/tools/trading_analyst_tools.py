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

"""Trading Analyst tools - Technical indicators from Alpha Vantage MCP"""

from .alpha_vantage_tools import get_alpha_vantage_mcp_toolset


def get_trading_analyst_tools():
    """
    Get technical analysis tools for Trading Analyst

    Returns Alpha Vantage MCP toolset which includes:
    - RSI (Relative Strength Index) - Momentum indicator
    - MACD (Moving Average Convergence Divergence) - Trend indicator
    - EMA (Exponential Moving Average) - Trend identification
    - BBANDS (Bollinger Bands) - Volatility indicator
    - STOCH (Stochastic Oscillator) - Momentum indicator
    - ADX (Average Directional Index) - Trend strength
    - OBV (On-Balance Volume) - Volume indicator
    - And 50+ other technical indicators

    The MCP server provides all these tools automatically.
    """
    return get_alpha_vantage_mcp_toolset()
