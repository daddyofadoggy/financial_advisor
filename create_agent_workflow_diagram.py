#!/usr/bin/env python3
"""
Generate Agent Workflow Diagram
Sequential flow matching deployment_steps.md Agent Workflow section
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

# Set up the figure
fig, ax = plt.subplots(figsize=(12, 16))
ax.set_xlim(0, 12)
ax.set_ylim(0, 16)
ax.axis('off')

# Color scheme
COLOR_USER = '#5F6368'  # Gray
COLOR_COORDINATOR = '#4285F4'  # Google Blue
COLOR_AGENT = '#34A853'  # Google Green
COLOR_MCP = '#FBBC04'  # Google Yellow
COLOR_OUTPUT = '#EA4335'  # Google Red

# Title
ax.text(6, 15.5, 'Agent Workflow', ha='center', va='top',
        fontsize=28, fontweight='bold')
ax.text(6, 15, 'Sequential Execution Flow', ha='center', va='top',
        fontsize=14, style='italic', color='#5F6368')

# ============================================================================
# STEP 1: USER INPUT
# ============================================================================
y_pos = 14

# User input box
user_box = FancyBboxPatch((3.5, y_pos - 0.5), 5, 1,
                          boxstyle="round,pad=0.15",
                          edgecolor=COLOR_USER, facecolor='#F8F9FA',
                          linewidth=3)
ax.add_patch(user_box)
ax.text(6, y_pos, 'User Input', ha='center', va='center',
        fontsize=16, fontweight='bold', color=COLOR_USER)
ax.text(6, y_pos - 0.25, '(Stock Ticker: e.g., AAPL, GOOGL)', ha='center', va='center',
        fontsize=10, style='italic')

# Arrow down
arrow = FancyArrowPatch((6, y_pos - 0.5), (6, y_pos - 1.2),
                       arrowstyle='->', mutation_scale=30, linewidth=3,
                       color=COLOR_USER)
ax.add_patch(arrow)

# ============================================================================
# STEP 2: FINANCIAL COORDINATOR
# ============================================================================
y_pos = y_pos - 2.5

coord_box = FancyBboxPatch((2.5, y_pos - 0.5), 7, 1,
                          boxstyle="round,pad=0.15",
                          edgecolor=COLOR_COORDINATOR, facecolor='#E8F0FE',
                          linewidth=4)
ax.add_patch(coord_box)
ax.text(6, y_pos + 0.15, 'Financial Coordinator', ha='center', va='center',
        fontsize=16, fontweight='bold', color=COLOR_COORDINATOR)
ax.text(6, y_pos - 0.2, 'Orchestrates sub-agents • Model: gemini-2.5-pro', ha='center', va='center',
        fontsize=10, style='italic')

# Arrow down
arrow = FancyArrowPatch((6, y_pos - 0.5), (6, y_pos - 1.2),
                       arrowstyle='->', mutation_scale=30, linewidth=3,
                       color=COLOR_COORDINATOR)
ax.add_patch(arrow)

# ============================================================================
# STEP 3: DATA ANALYST AGENT
# ============================================================================
y_pos = y_pos - 2.5

agent_box = FancyBboxPatch((2.5, y_pos - 0.8), 4.5, 1.6,
                          boxstyle="round,pad=0.15",
                          edgecolor=COLOR_AGENT, facecolor='#E6F4EA',
                          linewidth=3)
ax.add_patch(agent_box)
ax.text(4.75, y_pos + 0.4, 'Data Analyst', ha='center', va='center',
        fontsize=15, fontweight='bold', color=COLOR_AGENT)
ax.text(4.75, y_pos + 0.05, '(Market Data)', ha='center', va='center',
        fontsize=11, style='italic')
ax.text(4.75, y_pos - 0.35, 'Output: market_data_analysis_output', ha='center', va='center',
        fontsize=8, family='monospace', color=COLOR_OUTPUT)

# MCP connection box (to the right)
mcp_box = FancyBboxPatch((7.5, y_pos - 0.5), 4, 1,
                        boxstyle="round,pad=0.1",
                        edgecolor=COLOR_MCP, facecolor='#FEF7E0',
                        linewidth=3)
ax.add_patch(mcp_box)
ax.text(9.5, y_pos + 0.15, 'Alpha Vantage MCP', ha='center', va='center',
        fontsize=12, fontweight='bold', color=COLOR_MCP)
ax.text(9.5, y_pos - 0.2, '(60+ financial tools)', ha='center', va='center',
        fontsize=9, style='italic')

# Arrow from Data Analyst to MCP
mcp_arrow = FancyArrowPatch((7, y_pos), (7.5, y_pos),
                           arrowstyle='<->', mutation_scale=25, linewidth=2.5,
                           color=COLOR_MCP)
ax.add_patch(mcp_arrow)

# Arrow down
arrow = FancyArrowPatch((4.75, y_pos - 0.8), (4.75, y_pos - 1.5),
                       arrowstyle='->', mutation_scale=30, linewidth=3,
                       color=COLOR_AGENT)
ax.add_patch(arrow)
# Continue from center
arrow2 = FancyArrowPatch((4.75, y_pos - 1.5), (6, y_pos - 1.5),
                        arrowstyle='-', mutation_scale=30, linewidth=3,
                        color=COLOR_AGENT)
ax.add_patch(arrow2)
arrow3 = FancyArrowPatch((6, y_pos - 1.5), (6, y_pos - 2.0),
                        arrowstyle='->', mutation_scale=30, linewidth=3,
                        color=COLOR_AGENT)
ax.add_patch(arrow3)

# ============================================================================
# STEP 4: TRADING ANALYST AGENT
# ============================================================================
y_pos = y_pos - 3.5

agent_box = FancyBboxPatch((2.5, y_pos - 0.8), 7, 1.6,
                          boxstyle="round,pad=0.15",
                          edgecolor=COLOR_AGENT, facecolor='#E6F4EA',
                          linewidth=3)
ax.add_patch(agent_box)
ax.text(6, y_pos + 0.4, 'Trading Analyst', ha='center', va='center',
        fontsize=15, fontweight='bold', color=COLOR_AGENT)
ax.text(6, y_pos + 0.05, '(5+ Strategies)', ha='center', va='center',
        fontsize=11, style='italic')
ax.text(6, y_pos - 0.35, 'Output: proposed_trading_strategies_output', ha='center', va='center',
        fontsize=8, family='monospace', color=COLOR_OUTPUT)

# Arrow down
arrow = FancyArrowPatch((6, y_pos - 0.8), (6, y_pos - 1.5),
                       arrowstyle='->', mutation_scale=30, linewidth=3,
                       color=COLOR_AGENT)
ax.add_patch(arrow)

# ============================================================================
# STEP 5: EXECUTION ANALYST AGENT
# ============================================================================
y_pos = y_pos - 3

agent_box = FancyBboxPatch((2.5, y_pos - 0.8), 7, 1.6,
                          boxstyle="round,pad=0.15",
                          edgecolor=COLOR_AGENT, facecolor='#E6F4EA',
                          linewidth=3)
ax.add_patch(agent_box)
ax.text(6, y_pos + 0.4, 'Execution Analyst', ha='center', va='center',
        fontsize=15, fontweight='bold', color=COLOR_AGENT)
ax.text(6, y_pos + 0.05, '(Action Plan)', ha='center', va='center',
        fontsize=11, style='italic')
ax.text(6, y_pos - 0.35, 'Output: execution_plan_output', ha='center', va='center',
        fontsize=8, family='monospace', color=COLOR_OUTPUT)

# Arrow down
arrow = FancyArrowPatch((6, y_pos - 0.8), (6, y_pos - 1.5),
                       arrowstyle='->', mutation_scale=30, linewidth=3,
                       color=COLOR_AGENT)
ax.add_patch(arrow)

# ============================================================================
# STEP 6: RISK ANALYST AGENT
# ============================================================================
y_pos = y_pos - 3

agent_box = FancyBboxPatch((2.5, y_pos - 0.8), 7, 1.6,
                          boxstyle="round,pad=0.15",
                          edgecolor=COLOR_AGENT, facecolor='#E6F4EA',
                          linewidth=3)
ax.add_patch(agent_box)
ax.text(6, y_pos + 0.4, 'Risk Analyst', ha='center', va='center',
        fontsize=15, fontweight='bold', color=COLOR_AGENT)
ax.text(6, y_pos + 0.05, '(Risk Assessment)', ha='center', va='center',
        fontsize=11, style='italic')
ax.text(6, y_pos - 0.35, 'Output: final_risk_assessment_output', ha='center', va='center',
        fontsize=8, family='monospace', color=COLOR_OUTPUT)

# Arrow down
arrow = FancyArrowPatch((6, y_pos - 0.8), (6, y_pos - 1.5),
                       arrowstyle='->', mutation_scale=30, linewidth=3,
                       color=COLOR_AGENT)
ax.add_patch(arrow)

# ============================================================================
# STEP 7: SUMMARY AGENT
# ============================================================================
y_pos = y_pos - 3

agent_box = FancyBboxPatch((2.5, y_pos - 0.8), 7, 1.6,
                          boxstyle="round,pad=0.15",
                          edgecolor=COLOR_AGENT, facecolor='#E6F4EA',
                          linewidth=3)
ax.add_patch(agent_box)
ax.text(6, y_pos + 0.4, 'Summary Agent', ha='center', va='center',
        fontsize=15, fontweight='bold', color=COLOR_AGENT)
ax.text(6, y_pos + 0.05, '(Final Report)', ha='center', va='center',
        fontsize=11, style='italic')
ax.text(6, y_pos - 0.35, 'Output: executive_summary_output', ha='center', va='center',
        fontsize=8, family='monospace', color=COLOR_OUTPUT)

# Arrow down
arrow = FancyArrowPatch((6, y_pos - 0.8), (6, y_pos - 1.5),
                       arrowstyle='->', mutation_scale=30, linewidth=3,
                       color=COLOR_AGENT)
ax.add_patch(arrow)

# ============================================================================
# STEP 8: OUTPUT
# ============================================================================
y_pos = y_pos - 3

output_box = FancyBboxPatch((2, y_pos - 0.5), 8, 1,
                           boxstyle="round,pad=0.15",
                           edgecolor=COLOR_OUTPUT, facecolor='#FCE8E6',
                           linewidth=3)
ax.add_patch(output_box)
ax.text(6, y_pos + 0.15, 'PDF Export + Chat Display', ha='center', va='center',
        fontsize=16, fontweight='bold', color=COLOR_OUTPUT)
ax.text(6, y_pos - 0.2, 'Final financial analysis report delivered to user', ha='center', va='center',
        fontsize=10, style='italic')

# ============================================================================
# SIDE ANNOTATIONS
# ============================================================================

# State-based communication note
ax.text(11, 11, 'State-Based\nCommunication',
        ha='center', va='center', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FCE8E6',
                 edgecolor=COLOR_OUTPUT, linewidth=2))
ax.text(11, 10.2, 'Each agent writes\nits output to\nshared state',
        ha='center', va='center', fontsize=9, style='italic')

# Sequential execution note
ax.text(11, 7, 'Sequential\nExecution',
        ha='center', va='center', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#E6F4EA',
                 edgecolor=COLOR_AGENT, linewidth=2))
ax.text(11, 6.2, 'Agents execute\nin order,\none at a time',
        ha='center', va='center', fontsize=9, style='italic')

# Model info
ax.text(1, 11, 'All agents use\ngemini-2.5-pro',
        ha='center', va='center', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                 edgecolor='#5F6368', linewidth=1.5))

# ============================================================================
# LEGEND
# ============================================================================
legend_y = 1.5
ax.text(6, legend_y, 'Component Legend',
        ha='center', va='center', fontsize=12, fontweight='bold')

legend_items = [
    ('User Input/Output', COLOR_USER),
    ('Coordinator Agent', COLOR_COORDINATOR),
    ('Sub-Agents', COLOR_AGENT),
    ('External Tools (MCP)', COLOR_MCP),
    ('State Keys', COLOR_OUTPUT),
]

legend_x_start = 1.5
legend_spacing = 2.1
for i, (label, color) in enumerate(legend_items):
    x = legend_x_start + (i * legend_spacing)
    # Draw colored box
    box = Rectangle((x - 0.15, legend_y - 0.55), 0.3, 0.3,
                   facecolor=color, edgecolor=color, linewidth=2)
    ax.add_patch(box)
    # Draw label
    ax.text(x, legend_y - 0.9, label, ha='center', va='top',
            fontsize=8)

# Footer
ax.text(6, 0.3, 'Financial Advisor Multi-Agent System • Built with Google ADK • Powered by Gemini 2.5 Pro',
        ha='center', va='center', fontsize=9, style='italic', color='#5F6368')

# ============================================================================
# SAVE FIGURE
# ============================================================================
plt.tight_layout()
output_file = '/Users/ron/Documents/github/financial-advisor/agent_workflow_diagram.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Agent Workflow Diagram saved to: {output_file}")
plt.close()

print("\n📊 Agent Workflow Diagram Generated!")
print(f"📁 File location: {output_file}")
print(f"📐 Resolution: 300 DPI")
print(f"🎨 Shows: Sequential execution flow of all agents")
