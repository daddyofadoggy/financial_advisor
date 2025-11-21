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

"""Summary agent for generating executive summary and PDF export"""

from google.adk import Agent

from . import prompt

# Use same model as coordinator (known to work in your project)
MODEL = "gemini-2.5-pro"

summary_agent = Agent(
    model=MODEL,
    name="summary_agent",
    instruction=prompt.SUMMARY_AGENT_PROMPT,
    output_key="executive_summary_output",
)
