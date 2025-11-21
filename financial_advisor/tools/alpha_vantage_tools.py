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

"""Alpha Vantage MCP tools for financial data retrieval"""

import os
import threading
from typing import Any
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StreamableHTTPConnectionParams


class LazyMCPToolset:
    """
    A picklable lazy-loading wrapper for MCPToolset.

    This wrapper defers the actual MCP connection establishment until the toolset
    is actually used, making it safe to pickle for Agent Engines deployment.
    """

    # Add __name__ attribute for ADK compatibility
    __name__ = "AlphaVantageMCPToolset"

    def __init__(self):
        self._toolset = None
        self._lock = threading.Lock()

    def _ensure_initialized(self) -> MCPToolset:
        """Initialize the toolset if not already done."""
        if self._toolset is None:
            with self._lock:
                if self._toolset is None:
                    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

                    if not api_key:
                        # For deployment: Don't fail during initialization
                        # Just log a warning and return a placeholder
                        import warnings
                        warnings.warn(
                            "ALPHA_VANTAGE_API_KEY not found. "
                            "MCP tools will not be available until you configure the API key. "
                            "Set ALPHA_VANTAGE_API_KEY environment variable in your deployment."
                        )
                        # Return self to avoid errors, but tools won't work
                        return self

                    # Create connection parameters for Alpha Vantage HTTP MCP server
                    connection_params = StreamableHTTPConnectionParams(
                        url=f"https://mcp.alphavantage.co/mcp?apikey={api_key}"
                    )

                    # Connect to Alpha Vantage MCP server
                    self._toolset = MCPToolset(
                        connection_params=connection_params
                    )

        return self._toolset

    def __getstate__(self):
        """Return state for pickling (exclude the connection)."""
        return {}

    def __setstate__(self, state):
        """Restore state from pickling."""
        self._toolset = None
        self._lock = threading.Lock()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the underlying toolset."""
        toolset = self._ensure_initialized()
        return getattr(toolset, name)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Make the wrapper callable if needed."""
        toolset = self._ensure_initialized()
        if callable(toolset):
            return toolset(*args, **kwargs)
        return toolset


# Singleton instance
_alpha_vantage_toolset_instance = None
_toolset_lock = threading.Lock()


def get_alpha_vantage_mcp_toolset():
    """
    Get or create singleton Alpha Vantage MCP Toolset instance.

    This ensures only ONE connection to the Alpha Vantage MCP server is created
    and shared across all agents, reducing initialization overhead and API calls.

    The MCP server provides 60+ tools for financial market data including:
    - Real-time stock quotes (GLOBAL_QUOTE)
    - Company fundamentals (COMPANY_OVERVIEW)
    - Historical prices (TIME_SERIES_DAILY, TIME_SERIES_INTRADAY)
    - Technical indicators (RSI, MACD, EMA, BBANDS, STOCH, ADX, etc.)
    - News sentiment (NEWS_SENTIMENT)
    - And many more...

    Returns:
        MCPToolset: Alpha Vantage MCP toolset
    """
    global _alpha_vantage_toolset_instance

    # Thread-safe singleton pattern
    with _toolset_lock:
        if _alpha_vantage_toolset_instance is None:
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

            if not api_key:
                import warnings
                warnings.warn(
                    "ALPHA_VANTAGE_API_KEY not found. "
                    "MCP tools will not be available."
                )
                # Return a LazyMCPToolset that will handle missing key gracefully
                _alpha_vantage_toolset_instance = LazyMCPToolset()
            else:
                # Create connection parameters for Alpha Vantage HTTP MCP server
                connection_params = StreamableHTTPConnectionParams(
                    url=f"https://mcp.alphavantage.co/mcp?apikey={api_key}"
                )

                # Connect to Alpha Vantage MCP server directly (no wrapper needed for web deployment)
                _alpha_vantage_toolset_instance = MCPToolset(
                    connection_params=connection_params
                )

        return _alpha_vantage_toolset_instance


# Backward compatibility alias
def get_all_alpha_vantage_tools():
    """Get Alpha Vantage MCP toolset (backward compatible)"""
    return get_alpha_vantage_mcp_toolset()
