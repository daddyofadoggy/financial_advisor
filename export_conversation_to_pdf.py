#!/usr/bin/env python3
"""Export a conversation session JSON to PDF format."""

import json
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor


def parse_timestamp(timestamp_str):
    """Parse timestamp string to readable format."""
    try:
        # Parse ISO format timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp_str


def export_conversation_to_pdf(json_file, output_pdf):
    """Export conversation from JSON to PDF."""

    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create PDF document
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Container for PDF elements
    story = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_LEFT
    )

    user_style = ParagraphStyle(
        'UserMessage',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#0066cc'),
        spaceAfter=8,
        leftIndent=10,
        rightIndent=10,
        alignment=TA_LEFT
    )

    agent_style = ParagraphStyle(
        'AgentMessage',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#006600'),
        spaceAfter=8,
        leftIndent=10,
        rightIndent=10,
        alignment=TA_LEFT
    )

    timestamp_style = ParagraphStyle(
        'Timestamp',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#666666'),
        spaceAfter=4,
        alignment=TA_LEFT
    )

    separator_style = ParagraphStyle(
        'Separator',
        parent=styles['Normal'],
        fontSize=8,
        textColor=HexColor('#cccccc'),
        spaceAfter=12,
        spaceBefore=12
    )

    # Add title
    story.append(Paragraph("Conversation Export", title_style))
    story.append(Spacer(1, 0.2*inch))

    # Add session metadata
    metadata_text = f"<b>Session ID:</b> {data.get('id', 'N/A')}<br/>"
    metadata_text += f"<b>App Name:</b> {data.get('appName', 'N/A')}<br/>"
    metadata_text += f"<b>User ID:</b> {data.get('userId', 'N/A')}<br/>"
    metadata_text += f"<b>Last Update:</b> {parse_timestamp(data.get('lastUpdateTime', 'N/A'))}"

    story.append(Paragraph(metadata_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("─" * 80, separator_style))

    # Process events
    events = data.get('events', [])

    for idx, event in enumerate(events, 1):
        author = event.get('author', 'unknown')
        content = event.get('content', '')
        timestamp = event.get('timestamp', '')

        # Add event number and timestamp
        header = f"<b>Message {idx}</b> - {parse_timestamp(timestamp)}"
        story.append(Paragraph(header, timestamp_style))

        # Add author label
        if author.lower() == 'user':
            author_label = "<b>👤 User:</b>"
            message_style = user_style
        else:
            author_label = f"<b>🤖 Agent ({author}):</b>"
            message_style = agent_style

        story.append(Paragraph(author_label, message_style))

        # Add content
        # Escape special characters and preserve line breaks
        if content:
            # Replace newlines with HTML breaks
            content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            content = content.replace('\n', '<br/>')
            story.append(Paragraph(content, message_style))
        else:
            story.append(Paragraph("<i>(No content)</i>", message_style))

        # Add spacing between messages
        story.append(Spacer(1, 0.15*inch))
        story.append(Paragraph("─" * 80, separator_style))

    # Build PDF
    doc.build(story)
    print(f"✓ PDF exported successfully: {output_pdf}")
    print(f"  - Total messages: {len(events)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        json_file = "session-5eacfd80-33a5-4b48-96eb-1b01ee9fe045.json"
        output_pdf = "conversation_export.pdf"
    elif len(sys.argv) == 2:
        json_file = sys.argv[1]
        output_pdf = json_file.replace('.json', '.pdf')
    else:
        json_file = sys.argv[1]
        output_pdf = sys.argv[2]

    export_conversation_to_pdf(json_file, output_pdf)
