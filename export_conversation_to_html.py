#!/usr/bin/env python3
"""Export a conversation session JSON to HTML format (can be printed to PDF from browser)."""

import json
import sys
from datetime import datetime


def parse_timestamp(timestamp_str):
    """Parse timestamp string to readable format."""
    try:
        # Parse ISO format timestamp
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp_str


def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def markdown_to_html(text):
    """Convert basic Markdown formatting to HTML."""
    import re

    if not text:
        return ""

    # First escape HTML
    text = escape_html(text)

    # Convert headers (### Header -> <h3>Header</h3>)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Convert bold (**text** or __text__)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

    # Convert italic (*text* or _text_)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<em>\1</em>', text)

    # Convert inline code (`code`)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

    # Convert links [text](url)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', text)

    # Convert unordered lists (lines starting with -, *, or +)
    lines = text.split('\n')
    in_list = False
    result_lines = []

    for line in lines:
        # Check if line is a list item
        list_match = re.match(r'^[\s]*[-*+]\s+(.+)$', line)
        if list_match:
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(f'<li>{list_match.group(1)}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)

    if in_list:
        result_lines.append('</ul>')

    text = '\n'.join(result_lines)

    # Convert ordered lists (lines starting with numbers)
    lines = text.split('\n')
    in_ordered_list = False
    result_lines = []

    for line in lines:
        # Check if line is an ordered list item
        ordered_match = re.match(r'^[\s]*\d+\.\s+(.+)$', line)
        if ordered_match:
            if not in_ordered_list:
                result_lines.append('<ol>')
                in_ordered_list = True
            result_lines.append(f'<li>{ordered_match.group(1)}</li>')
        else:
            if in_ordered_list:
                result_lines.append('</ol>')
                in_ordered_list = False
            result_lines.append(line)

    if in_ordered_list:
        result_lines.append('</ol>')

    text = '\n'.join(result_lines)

    return text


def extract_message_content(event):
    """Extract message content including user messages, agent responses, and A2A outputs."""
    author = event.get('author', 'unknown')
    content = event.get('content', {})
    parts = content.get('parts', [])

    messages = []

    for part in parts:
        if not isinstance(part, dict):
            continue

        # User message text
        if author.lower() == 'user' and 'text' in part:
            messages.append({
                'type': 'user',
                'content': part['text'],
                'agent_name': None
            })

        # Agent visible response (not thinking)
        elif ('text' in part and
              'thoughtSignature' not in part and
              author.lower() != 'user'):
            messages.append({
                'type': 'agent_response',
                'content': part['text'],
                'agent_name': author
            })

        # Agent-to-Agent output (functionResponse)
        elif 'functionResponse' in part:
            func_response = part['functionResponse']
            agent_name = func_response.get('name', 'unknown_agent')
            response_data = func_response.get('response', {})

            # Extract the result from the agent
            if 'result' in response_data:
                messages.append({
                    'type': 'agent_output',
                    'content': response_data['result'],
                    'agent_name': agent_name
                })

    return messages


def format_agent_name(agent_name):
    """Format agent name for display."""
    if not agent_name:
        return "Assistant"

    # Convert snake_case to Title Case
    name = agent_name.replace('_', ' ').title()
    # Remove '_agent' suffix if present
    name = name.replace(' Agent', '')
    return name


def export_conversation_to_html(json_file, output_html):
    """Export conversation from JSON to HTML."""

    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Start HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversation Export</title>
    <style>
        @media print {
            body { margin: 0.5in; }
            .message { page-break-inside: avoid; }
            .print-button { display: none; }
            .metadata { page-break-after: avoid; }
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #1a1a1a;
            line-height: 1.6;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1a1a1a;
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: 600;
        }
        .subtitle {
            color: #65676b;
            font-size: 14px;
            margin-bottom: 25px;
        }
        .metadata {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0 30px 0;
            font-size: 13px;
            border-left: 4px solid #0084ff;
        }
        .metadata p {
            margin: 5px 0;
            color: #586069;
        }
        .metadata strong {
            color: #24292e;
            font-weight: 600;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .message {
            display: flex;
            flex-direction: column;
            margin: 8px 0;
        }
        .message.user {
            align-items: flex-end;
        }
        .message.agent, .message.agent-output {
            align-items: flex-start;
        }
        .message-bubble {
            max-width: 90%;
            padding: 14px 18px;
            border-radius: 12px;
            position: relative;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        .message.user .message-bubble {
            background-color: #0084ff;
            color: white;
            border-bottom-right-radius: 4px;
        }
        .message.agent .message-bubble {
            background-color: #f0f0f0;
            color: #1a1a1a;
            border-bottom-left-radius: 4px;
        }
        .message.agent-output .message-bubble {
            background-color: #e8f5e9;
            color: #1a1a1a;
            border-bottom-left-radius: 4px;
            border-left: 3px solid #4caf50;
        }
        .author-label {
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 6px;
            padding: 0 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .message.user .author-label {
            color: #0084ff;
            justify-content: flex-end;
        }
        .message.agent .author-label {
            color: #65676b;
        }
        .message.agent-output .author-label {
            color: #2e7d32;
        }
        .agent-badge {
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
        }
        .timestamp {
            font-size: 11px;
            color: #999;
            margin-top: 4px;
            padding: 0 6px;
        }
        .message.user .timestamp {
            text-align: right;
        }
        .content {
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 14px;
            line-height: 1.6;
        }
        .content h1 {
            font-size: 20px;
            font-weight: 600;
            margin: 12px 0 8px 0;
            color: inherit;
        }
        .content h2 {
            font-size: 18px;
            font-weight: 600;
            margin: 10px 0 6px 0;
            color: inherit;
        }
        .content h3 {
            font-size: 16px;
            font-weight: 600;
            margin: 8px 0 4px 0;
            color: inherit;
        }
        .content strong {
            font-weight: 600;
        }
        .content em {
            font-style: italic;
        }
        .content code {
            background-color: rgba(0,0,0,0.05);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 13px;
        }
        .message.user .content code {
            background-color: rgba(255,255,255,0.2);
        }
        .content ul, .content ol {
            margin: 8px 0;
            padding-left: 24px;
        }
        .content li {
            margin: 4px 0;
        }
        .content a {
            color: #0084ff;
            text-decoration: underline;
        }
        .message.user .content a {
            color: #ffffff;
        }
        .print-button {
            background-color: #0084ff;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            margin: 20px 0;
            transition: background-color 0.2s;
        }
        .print-button:hover {
            background-color: #0073e6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💬 Conversation Export</h1>
        <div class="subtitle">Multi-Agent Financial Advisor Conversation</div>

        <button class="print-button" onclick="window.print()">🖨️ Print to PDF</button>
"""

    # Add metadata
    html += '<div class="metadata">\n'
    html += f'<p><strong>Session ID:</strong> {escape_html(data.get("id", "N/A"))}</p>\n'
    html += f'<p><strong>App Name:</strong> {escape_html(data.get("appName", "N/A"))}</p>\n'
    html += f'<p><strong>User ID:</strong> {escape_html(data.get("userId", "N/A"))}</p>\n'
    html += f'<p><strong>Last Update:</strong> {parse_timestamp(data.get("lastUpdateTime", "N/A"))}</p>\n'
    html += '</div>\n'

    html += '<div class="chat-container">\n'

    # Process events
    events = data.get('events', [])
    message_count = 0

    for event in events:
        timestamp = event.get('timestamp', '')
        messages = extract_message_content(event)

        for msg in messages:
            message_count += 1
            msg_type = msg['type']
            content = msg['content']
            agent_name = msg.get('agent_name')

            if msg_type == 'user':
                html += '<div class="message user">\n'
                html += '  <div class="author-label">You</div>\n'
                html += '  <div class="message-bubble">\n'
                html += f'    <div class="content">{markdown_to_html(content)}</div>\n'
                html += '  </div>\n'
                html += f'  <div class="timestamp">{parse_timestamp(timestamp)}</div>\n'
                html += '</div>\n\n'

            elif msg_type == 'agent_response':
                html += '<div class="message agent">\n'
                html += f'  <div class="author-label">{format_agent_name(agent_name)}</div>\n'
                html += '  <div class="message-bubble">\n'
                html += f'    <div class="content">{markdown_to_html(content)}</div>\n'
                html += '  </div>\n'
                html += f'  <div class="timestamp">{parse_timestamp(timestamp)}</div>\n'
                html += '</div>\n\n'

            elif msg_type == 'agent_output':
                html += '<div class="message agent-output">\n'
                html += f'  <div class="author-label"><span class="agent-badge">🤖 {format_agent_name(agent_name)}</span></div>\n'
                html += '  <div class="message-bubble">\n'
                html += f'    <div class="content">{markdown_to_html(content)}</div>\n'
                html += '  </div>\n'
                html += f'  <div class="timestamp">{parse_timestamp(timestamp)}</div>\n'
                html += '</div>\n\n'

    html += '</div>\n'  # Close chat-container

    # Close HTML
    html += """    </div>
</body>
</html>
"""

    # Write HTML file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Conversation exported successfully: {output_html}")
    print(f"  - Total messages: {message_count}")
    print(f"\nTo convert to PDF:")
    print(f"  1. Open {output_html} in your web browser")
    print(f"  2. Click the 'Print to PDF' button or press Cmd+P (Mac) / Ctrl+P (Windows)")
    print(f"  3. Select 'Save as PDF' as the destination")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        json_file = "session-5eacfd80-33a5-4b48-96eb-1b01ee9fe045.json"
        output_html = "conversation_export.html"
    elif len(sys.argv) == 2:
        json_file = sys.argv[1]
        output_html = json_file.replace('.json', '.html')
    else:
        json_file = sys.argv[1]
        output_html = sys.argv[2]

    export_conversation_to_html(json_file, output_html)
