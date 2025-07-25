#!/usr/bin/env python3
"""
Simple Overlay Generator CLI

Usage: python generate_overlay.py "your prompt here"
Example: python generate_overlay.py "create a sticky note overlay"
"""

import sys
import os
import json
from overlay_agent_dir.overlay_agent import generate_website_overlay_js

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_overlay.py \"your prompt here\"")
        print("Example: python generate_overlay.py \"create a sticky note overlay\"")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    print(f"🎯 Generating overlay for: {prompt}")
    print("=" * 50)
    
    # Generate the JavaScript code
    js_code = generate_website_overlay_js(prompt)
    
    # Check if there was an error
    if js_code.startswith('{"error"'):
        error_data = json.loads(js_code)
        print("❌ Error:", error_data["error"])
        print("\n💡 Make sure your OPENAI_API_KEY is set in overlay_agent_dir/.env")
        sys.exit(1)
    
    print("✅ JavaScript code generated successfully!")
    print("\n📋 Copy the code below and paste it into your browser's developer console:")
    print("-" * 70)
    print(js_code)
    print("-" * 70)
    print("\n🚀 Instructions:")
    print("1. Open your browser's developer console (F12 or Cmd+Option+I)")
    print("2. Copy the JavaScript code above")
    print("3. Paste it into the console and press Enter")
    print("4. The overlay should appear on your webpage!")

if __name__ == "__main__":
    main() 