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

"""Execution Analyst tools - Liquidity and execution analysis from Alpha Vantage MCP"""

from .alpha_vantage_tools import get_alpha_vantage_mcp_toolset


def get_execution_analyst_tools():
    """
    Get execution analysis tools for Execution Analyst

    Returns Alpha Vantage MCP toolset which includes:
    - TIME_SERIES_INTRADAY - Intraday price patterns for timing
    - GLOBAL_QUOTE - Real-time bid-ask spread for slippage estimation
    - VWAP - Volume Weighted Average Price for benchmarking
    - OBV - On-Balance Volume for liquidity assessment
    - Historical volume data - Average daily volume calculation
    - Market status - Trading hours and optimal execution windows

    The MCP server provides all these tools automatically.
    """
    return get_alpha_vantage_mcp_toolset()
