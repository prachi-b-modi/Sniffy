#!/usr/bin/env python3
"""
Python client for interacting with the ADK overlay agent API server
"""

import requests
import json
import time
from typing import Dict, Any, Optional

class ADKClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        Initialize the ADK client
        
        Args:
            base_url: Base URL of the ADK API server
        """
        self.base_url = base_url
        self.session = requests.Session()
        
    def generate_overlay_js(self, prompt: str, user_id: str = "user123", app_name: str = "overlay_generator", timeout: int = 30) -> Dict[str, Any]:
        """
        Send a prompt to the ADK agent and get JavaScript code back
        
        Args:
            prompt: The user's request for overlay/modification
            user_id: Unique identifier for the user
            app_name: Name of the ADK app
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary containing the response with JavaScript code
        """
        try:
            # Create session using the correct ADK API structure
            session_response = self.session.post(
                f"{self.base_url}/apps/{app_name}/users/{user_id}/sessions",
                json={},
                timeout=timeout
            )
            session_response.raise_for_status()
            session_data = session_response.json()
            session_id = session_data["id"]
            
            # Send message to agent using the correct payload structure
            message_payload = {
                "appName": app_name,
                "userId": user_id,
                "sessionId": session_id,
                "newMessage": {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/run",
                json=message_payload,
                timeout=timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract JavaScript code from response
            # The response might be in different formats, let's handle multiple possibilities
            raw_response = ""
            if "content" in result and "parts" in result["content"] and len(result["content"]["parts"]) > 0:
                raw_response = result["content"]["parts"][0].get("text", "")
            elif "response" in result:
                raw_response = result["response"]
            elif "message" in result:
                raw_response = result["message"]
            else:
                raw_response = str(result)
            
            js_code = self._extract_javascript_from_markdown(raw_response)
            return {
                "success": True,
                "javascript": js_code,
                "session_id": session_id,
                "app_name": app_name,
                "raw_response": result
            }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "raw_response": None
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON decode error: {str(e)}",
                "raw_response": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "raw_response": None
            }

    def _extract_javascript_from_markdown(self, text: str) -> str:
        """
        Extract JavaScript code from markdown code blocks
        
        Args:
            text: Raw text that may contain markdown code blocks
            
        Returns:
            Extracted JavaScript code or original text if no code blocks found
        """
        import re
        
        # Pattern to match markdown code blocks with optional language specifier
        # Matches: ```javascript\n<code>\n``` or ```js\n<code>\n``` or ```\n<code>\n```
        patterns = [
            r'```(?:javascript|js)\s*\n(.*?)\n```',  # ```javascript or ```js
            r'```\s*\n(.*?)\n```',                   # ``` without language
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                extracted_code = match.group(1).strip()
                if extracted_code:  # Only return if we found actual code
                    return extracted_code
        
        # If no markdown code blocks found, return the original text
        return text.strip()

    def health_check(self) -> Dict[str, Any]:
        """
        Check if the ADK API server is healthy
        
        Returns:
            Dictionary with health status
        """
        try:
            # Use /list-apps endpoint to check if server is responding
            response = self.session.get(f"{self.base_url}/list-apps", timeout=5)
            response.raise_for_status()
            return {
                "success": True,
                "status": "healthy",
                "apps": response.json()
            }
        except Exception as e:
            return {
                "success": False,
                "status": "unhealthy",
                "error": str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = ADKClient("http://localhost:8080")
    
    # Test health check
    print("🏥 Health Check:")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    if health["success"]:
        print("\n🚀 Testing overlay generation...")
        
        # Test cases
        test_prompts = [
            "change bg to red",
            "create an overlay",
            "add a note",
            "change background to blue"
        ]
        
        for prompt in test_prompts:
            print(f"\n📝 Prompt: '{prompt}'")
            result = client.generate_overlay_js(prompt)
            
            if result["success"]:
                print("✅ Success!")
                print(f"JavaScript code preview: {result['javascript'][:100]}...")
                
                # Save to file for testing
                filename = f"generated_{prompt.replace(' ', '_')}.js"
                with open(filename, 'w') as f:
                    f.write(result['javascript'])
                print(f"💾 Saved to: {filename}")
            else:
                print(f"❌ Failed: {result['error']}")
    else:
        print("❌ ADK server is not healthy. Make sure it's running!") 