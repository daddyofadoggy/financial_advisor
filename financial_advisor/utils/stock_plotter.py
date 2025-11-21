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

"""Stock trend plotting utility"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import re


def parse_price_trend_from_analysis(market_analysis: str) -> dict:
    """
    Extract price trend data from market analysis output

    Args:
        market_analysis: The market_data_analysis_output text

    Returns:
        dict: Dictionary with ticker, current_price, trend_description, and price_data
    """
    result = {
        "ticker": "STOCK",
        "current_price": 0.0,
        "trend_description": "No trend data available",
        "price_change_30d": None
    }

    # Extract ticker symbol
    ticker_match = re.search(r'Market Analysis Report for:\s*(\w+)', market_analysis)
    if ticker_match:
        result["ticker"] = ticker_match.group(1)

    # Extract current price
    price_match = re.search(r'Current Stock Price:\s*\$?([\d,]+\.?\d*)', market_analysis)
    if price_match:
        result["current_price"] = float(price_match.group(1).replace(',', ''))

    # Extract 30-day trend
    trend_match = re.search(r'Price Trend \(Last 30 Days\):\s*([^\n]+)', market_analysis)
    if trend_match:
        result["trend_description"] = trend_match.group(1).strip()

    # Extract price change and percent
    change_match = re.search(r'Price Change:\s*\$?([-\d,]+\.?\d*)\s*\(([-\d.]+)%\)', market_analysis)
    if change_match:
        result["price_change_30d"] = {
            "change": float(change_match.group(1).replace(',', '')),
            "percent": float(change_match.group(2))
        }

    return result


def plot_stock_trend(market_analysis: str, save_path: str = None) -> str:
    """
    Create a stock trend plot from market analysis data

    Args:
        market_analysis: The market_data_analysis_output text
        save_path: Optional path to save the plot

    Returns:
        str: Path to the saved plot image
    """
    # Parse the analysis data
    data = parse_price_trend_from_analysis(market_analysis)

    ticker = data["ticker"]
    current_price = data["current_price"]
    trend_desc = data["trend_description"]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Since we don't have actual historical data points, create a simple visualization
    # showing current price and trend direction based on the analysis

    # Create a simple trend line based on description
    if current_price > 0:
        # Determine trend direction from description
        is_uptrend = any(word in trend_desc.lower() for word in ['up', 'gain', 'increase', 'rising', 'bullish', 'positive'])
        is_downtrend = any(word in trend_desc.lower() for word in ['down', 'loss', 'decrease', 'falling', 'bearish', 'negative'])

        # Generate sample data points for visualization
        days = list(range(30))

        if data["price_change_30d"]:
            # Use actual price change data
            price_change = data["price_change_30d"]["change"]
            start_price = current_price - price_change
            prices = [start_price + (price_change * (i/29)) for i in days]
        elif is_uptrend:
            # Simulate uptrend
            start_price = current_price * 0.95
            prices = [start_price + ((current_price - start_price) * (i/29)) for i in days]
        elif is_downtrend:
            # Simulate downtrend
            start_price = current_price * 1.05
            prices = [start_price - ((start_price - current_price) * (i/29)) for i in days]
        else:
            # Sideways/stable
            prices = [current_price * (0.995 + 0.01 * (i % 3) / 2) for i in days]

        # Plot the trend
        ax.plot(days, prices, linewidth=2, color='#1f77b4', label=f'{ticker} Price')
        ax.scatter([29], [current_price], color='red', s=100, zorder=5, label=f'Current: ${current_price:.2f}')

        # Add grid
        ax.grid(True, alpha=0.3, linestyle='--')

        # Formatting
        ax.set_xlabel('Days Ago', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_title(f'{ticker} - 30-Day Price Trend\n{trend_desc}', fontsize=14, fontweight='bold')
        ax.legend(loc='best')

        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))

        # Invert x-axis to show "30 days ago" on left
        ax.invert_xaxis()
        ax.set_xlabel('Days Ago (0 = Today)', fontsize=12)

        # Add trend indicator box
        trend_color = 'green' if is_uptrend else 'red' if is_downtrend else 'gray'
        trend_label = '▲ UPTREND' if is_uptrend else '▼ DOWNTREND' if is_downtrend else '→ SIDEWAYS'

        ax.text(0.02, 0.98, trend_label, transform=ax.transAxes,
                fontsize=12, fontweight='bold', color=trend_color,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    else:
        ax.text(0.5, 0.5, 'Price data not available',
                ha='center', va='center', fontsize=14, transform=ax.transAxes)

    plt.tight_layout()

    # Save the plot
    if not save_path:
        import os
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        downloads_dir = os.path.expanduser("~/Downloads")
        if os.path.exists(downloads_dir):
            save_path = os.path.join(downloads_dir, f"stock_trend_{ticker}_{timestamp}.png")
        else:
            save_path = f"stock_trend_{ticker}_{timestamp}.png"

    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    return save_path
