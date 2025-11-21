#!/usr/bin/env python3
"""
Generate Multi-Agent Architecture Diagram
Shows agent collaboration via A2A, MCP, and state-based communication
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.patches import Rectangle
import numpy as np

# Set up the figure
fig, ax = plt.subplots(figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

# Color scheme
COLOR_COORDINATOR = '#4285F4'  # Google Blue
COLOR_AGENT = '#34A853'  # Google Green
COLOR_MCP = '#FBBC04'  # Google Yellow
COLOR_STATE = '#EA4335'  # Google Red
COLOR_TOOL = '#9334E6'  # Purple
COLOR_USER = '#5F6368'  # Gray

# Title
ax.text(10, 13.5, 'Financial Advisor Multi-Agent Architecture',
        ha='center', va='top', fontsize=24, fontweight='bold')
ax.text(10, 13, 'State-Based Communication • Agent-to-Agent (A2A) • Model Context Protocol (MCP)',
        ha='center', va='top', fontsize=12, style='italic', color='#5F6368')

# ============================================================================
# USER INPUT
# ============================================================================
user_box = FancyBboxPatch((8.5, 11.5), 3, 0.8,
                          boxstyle="round,pad=0.1",
                          edgecolor=COLOR_USER, facecolor='#F8F9FA',
                          linewidth=3)
ax.add_patch(user_box)
ax.text(10, 11.9, '👤 User Query', ha='center', va='center',
        fontsize=14, fontweight='bold')

# Arrow from user to coordinator
arrow = FancyArrowPatch((10, 11.5), (10, 10.5),
                       arrowstyle='->', mutation_scale=30, linewidth=2.5,
                       color=COLOR_USER)
ax.add_patch(arrow)

# ============================================================================
# FINANCIAL COORDINATOR (Root Agent)
# ============================================================================
coord_box = FancyBboxPatch((7, 9.5), 6, 1,
                          boxstyle="round,pad=0.1",
                          edgecolor=COLOR_COORDINATOR, facecolor='#E8F0FE',
                          linewidth=4)
ax.add_patch(coord_box)
ax.text(10, 10.3, '🎯 Financial Coordinator', ha='center', va='center',
        fontsize=16, fontweight='bold', color=COLOR_COORDINATOR)
ax.text(10, 9.9, 'Root Agent • Orchestrates Sub-Agents via A2A',
        ha='center', va='center', fontsize=10, style='italic')
ax.text(10, 9.6, 'Model: gemini-2.5-pro',
        ha='center', va='center', fontsize=9, color='#5F6368')

# ============================================================================
# STATE STORAGE (Central)
# ============================================================================
state_box = FancyBboxPatch((8, 7.5), 4, 1.5,
                          boxstyle="round,pad=0.1",
                          edgecolor=COLOR_STATE, facecolor='#FCE8E6',
                          linewidth=3, linestyle='--')
ax.add_patch(state_box)
ax.text(10, 8.85, '📊 Shared State Storage', ha='center', va='center',
        fontsize=14, fontweight='bold', color=COLOR_STATE)

state_keys = [
    'market_data_analysis_output',
    'proposed_trading_strategies_output',
    'execution_plan_output',
    'final_risk_assessment_output',
    'executive_summary_output'
]
y_pos = 8.5
for key in state_keys:
    ax.text(10, y_pos, f'• {key}', ha='center', va='center',
            fontsize=7, family='monospace')
    y_pos -= 0.15

# ============================================================================
# SUB-AGENTS (5 agents in two rows)
# ============================================================================

# Row 1: Data Analyst, Trading Analyst, Execution Analyst
agents_row1 = [
    {
        'name': 'Data Analyst',
        'icon': '📈',
        'x': 1,
        'y': 5,
        'output': 'market_data_analysis_output',
        'has_mcp': True,
        'description': 'Retrieves market data\nvia MCP tools'
    },
    {
        'name': 'Trading Analyst',
        'icon': '💹',
        'x': 7,
        'y': 5,
        'output': 'proposed_trading_strategies_output',
        'has_mcp': False,
        'description': 'Develops trading\nstrategies'
    },
    {
        'name': 'Execution Analyst',
        'icon': '⚡',
        'x': 13,
        'y': 5,
        'output': 'execution_plan_output',
        'has_mcp': False,
        'description': 'Creates execution\nplans'
    }
]

# Row 2: Risk Analyst, Summary Agent
agents_row2 = [
    {
        'name': 'Risk Analyst',
        'icon': '⚠️',
        'x': 4,
        'y': 2,
        'output': 'final_risk_assessment_output',
        'has_mcp': False,
        'description': 'Evaluates overall\nrisk'
    },
    {
        'name': 'Summary Agent',
        'icon': '📝',
        'x': 10,
        'y': 2,
        'output': 'executive_summary_output',
        'has_mcp': False,
        'description': 'Generates executive\nsummary'
    }
]

def draw_agent(agent_info):
    """Draw an agent box with details"""
    x, y = agent_info['x'], agent_info['y']

    # Agent box
    box = FancyBboxPatch((x, y), 4, 1.8,
                         boxstyle="round,pad=0.1",
                         edgecolor=COLOR_AGENT, facecolor='#E6F4EA',
                         linewidth=3)
    ax.add_patch(box)

    # Agent name
    ax.text(x + 2, y + 1.5, f'{agent_info["icon"]} {agent_info["name"]}',
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=COLOR_AGENT)

    # Description
    ax.text(x + 2, y + 1.1, agent_info['description'],
            ha='center', va='center', fontsize=8)

    # Output key
    ax.text(x + 2, y + 0.6, '🔑 Output:', ha='center', va='center',
            fontsize=8, fontweight='bold')
    ax.text(x + 2, y + 0.35, agent_info['output'][:25] + '...',
            ha='center', va='center', fontsize=7, family='monospace',
            color=COLOR_STATE)

    # Model
    ax.text(x + 2, y + 0.1, 'Model: gemini-2.5-pro',
            ha='center', va='center', fontsize=7, color='#5F6368')

    return x + 2, y

# Draw all agents
for agent in agents_row1 + agents_row2:
    draw_agent(agent)

# ============================================================================
# A2A CONNECTIONS (Coordinator to Agents via AgentTool)
# ============================================================================
ax.text(10, 9.2, 'A2A Communication via AgentTool', ha='center', va='center',
        fontsize=9, fontweight='bold', color=COLOR_COORDINATOR,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLOR_COORDINATOR))

# Arrows from Coordinator to each agent
agent_centers = [
    (3, 5.9),   # Data Analyst
    (9, 5.9),   # Trading Analyst
    (15, 5.9),  # Execution Analyst
    (6, 2.9),   # Risk Analyst
    (12, 2.9),  # Summary Agent
]

for i, (ax_pos, ay_pos) in enumerate(agent_centers):
    # A2A arrow from coordinator to agent
    arrow = FancyArrowPatch((10, 9.5), (ax_pos, ay_pos + 1.8),
                           arrowstyle='->', mutation_scale=20, linewidth=2,
                           color=COLOR_COORDINATOR, linestyle='--',
                           connectionstyle="arc3,rad=0.3")
    ax.add_patch(arrow)

    # State write arrow from agent to state storage
    arrow_state = FancyArrowPatch((ax_pos, ay_pos + 1.8), (10, 8.5 if i < 3 else 7.7),
                                 arrowstyle='->', mutation_scale=15, linewidth=1.5,
                                 color=COLOR_STATE, alpha=0.6,
                                 connectionstyle="arc3,rad=-0.2")
    ax.add_patch(arrow_state)

# ============================================================================
# MCP CONNECTION (Data Analyst to Alpha Vantage)
# ============================================================================

# Alpha Vantage MCP Server box
mcp_box = FancyBboxPatch((0.5, 3), 4.5, 1.5,
                         boxstyle="round,pad=0.1",
                         edgecolor=COLOR_MCP, facecolor='#FEF7E0',
                         linewidth=3)
ax.add_patch(mcp_box)
ax.text(2.75, 4.2, '🌐 Alpha Vantage MCP Server', ha='center', va='center',
        fontsize=11, fontweight='bold', color=COLOR_MCP)
ax.text(2.75, 3.85, 'Model Context Protocol', ha='center', va='center',
        fontsize=9, style='italic')

# MCP Tools list
tools = [
    'GLOBAL_QUOTE',
    'COMPANY_OVERVIEW',
    'TIME_SERIES_DAILY',
    'NEWS_SENTIMENT',
    '...60+ tools'
]
y_tool = 3.6
for tool in tools:
    ax.text(2.75, y_tool, f'• {tool}', ha='center', va='center',
            fontsize=7, family='monospace')
    y_tool -= 0.13

# MCP connection arrow
mcp_arrow = FancyArrowPatch((3, 5), (3, 4.5),
                           arrowstyle='<->', mutation_scale=25, linewidth=3,
                           color=COLOR_MCP)
ax.add_patch(mcp_arrow)
ax.text(3.3, 4.75, 'MCP\nConnection', ha='left', va='center',
        fontsize=8, fontweight='bold', color=COLOR_MCP,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=COLOR_MCP))

# ============================================================================
# ADDITIONAL TOOLS
# ============================================================================

# PDF Export Tool
pdf_box = FancyBboxPatch((15.5, 3), 4, 1.5,
                         boxstyle="round,pad=0.1",
                         edgecolor=COLOR_TOOL, facecolor='#F3E8FF',
                         linewidth=3)
ax.add_patch(pdf_box)
ax.text(17.5, 4.2, '🔧 Visualization Tools', ha='center', va='center',
        fontsize=11, fontweight='bold', color=COLOR_TOOL)
ax.text(17.5, 3.85, 'Additional Tools', ha='center', va='center',
        fontsize=9, style='italic')
ax.text(17.5, 3.5, '• export_summary_to_pdf', ha='center', va='center',
        fontsize=8, family='monospace')
ax.text(17.5, 3.3, '• Chart generation', ha='center', va='center',
        fontsize=8, family='monospace')

# Tool connection to coordinator
tool_arrow = FancyArrowPatch((13, 9.8), (15.5, 4.2),
                            arrowstyle='<->', mutation_scale=20, linewidth=2,
                            color=COLOR_TOOL, linestyle='--',
                            connectionstyle="arc3,rad=-0.3")
ax.add_patch(tool_arrow)

# ============================================================================
# SEQUENTIAL FLOW INDICATORS
# ============================================================================
ax.text(1, 0.8, 'Sequential Agent Execution Flow:', ha='left', va='center',
        fontsize=10, fontweight='bold', color='#5F6368')

flow_steps = [
    '1️⃣ Data Analyst → Market Analysis',
    '2️⃣ Trading Analyst → Strategy Development',
    '3️⃣ Execution Analyst → Execution Planning',
    '4️⃣ Risk Analyst → Risk Assessment',
    '5️⃣ Summary Agent → Executive Summary'
]

y_flow = 0.5
for step in flow_steps:
    ax.text(1, y_flow, step, ha='left', va='center', fontsize=8, color='#5F6368')
    y_flow -= 0.15

# ============================================================================
# LEGEND
# ============================================================================
legend_x = 13
legend_y = 1.2

ax.text(legend_x, legend_y, 'Legend:', ha='left', va='center',
        fontsize=10, fontweight='bold', color='#5F6368')

legend_items = [
    ('A2A (Agent-to-Agent)', COLOR_COORDINATOR, '--'),
    ('State Communication', COLOR_STATE, '-'),
    ('MCP Connection', COLOR_MCP, '-'),
    ('Tool Access', COLOR_TOOL, '--'),
]

y_legend = legend_y - 0.2
for label, color, style in legend_items:
    # Draw line
    ax.plot([legend_x, legend_x + 0.4], [y_legend, y_legend],
            color=color, linewidth=2, linestyle=style)
    # Draw label
    ax.text(legend_x + 0.5, y_legend, label, ha='left', va='center',
            fontsize=8, color='#5F6368')
    y_legend -= 0.15

# ============================================================================
# ANNOTATIONS
# ============================================================================

# State-based communication annotation
ax.annotate('Agents write outputs to shared state',
            xy=(10, 7.5), xytext=(10, 6.5),
            ha='center', fontsize=9, color=COLOR_STATE,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                     edgecolor=COLOR_STATE, alpha=0.8),
            arrowprops=dict(arrowstyle='->', color=COLOR_STATE, lw=2))

# A2A annotation
ax.annotate('Coordinator invokes agents\nvia AgentTool (A2A)',
            xy=(10, 9.5), xytext=(15.5, 9),
            ha='left', fontsize=9, color=COLOR_COORDINATOR,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                     edgecolor=COLOR_COORDINATOR, alpha=0.8),
            arrowprops=dict(arrowstyle='->', color=COLOR_COORDINATOR, lw=2))

# MCP annotation
ax.annotate('External data via\nMCP protocol',
            xy=(2.75, 4.5), xytext=(0.5, 6.5),
            ha='left', fontsize=9, color=COLOR_MCP,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                     edgecolor=COLOR_MCP, alpha=0.8),
            arrowprops=dict(arrowstyle='->', color=COLOR_MCP, lw=2))

# Footer
ax.text(10, 0.05, 'Built with Google ADK • Deployed on Google Cloud Run • Powered by Gemini 2.5 Pro',
        ha='center', va='bottom', fontsize=9, style='italic', color='#5F6368')

# ============================================================================
# SAVE FIGURE
# ============================================================================
plt.tight_layout()
output_file = '/Users/ron/Documents/github/financial-advisor/multi_agent_architecture.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Diagram saved to: {output_file}")
plt.close()

print("\n📊 Multi-Agent Architecture Diagram Generated!")
print(f"📁 File location: {output_file}")
print(f"📐 Resolution: 300 DPI")
print(f"🎨 Shows: A2A communication, MCP integration, and state-based collaboration")
