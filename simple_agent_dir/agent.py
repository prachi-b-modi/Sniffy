#!/usr/bin/env python3
"""
Simple test agent without custom tools
"""

from google.adk.agents import Agent

# Simple agent without tools
root_agent = Agent(
    name="simple_test_agent",
    model="gemini-2.0-flash",
    description="A simple test agent without custom tools",
    instruction="You are a helpful assistant. Just respond to user messages normally."
) 