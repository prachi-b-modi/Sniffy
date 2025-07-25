# ADK Overlay Agent API Integration Guide

This guide shows you how to integrate your ADK overlay agent with any application using the REST API.

## 🚀 Quick Start

### 1. Start the ADK API Server
```bash
# Terminal 1: Start ADK API server
adk api_server overlay_agent_dir --port 8080
```

### 2. Test with Python Client
```bash
# Terminal 2: Test the API
python adk_client.py
```

### 3. Test with cURL
```bash
# Make the script executable and run it
chmod +x curl_examples.sh
./curl_examples.sh
```

### 4. Try the Example Web App
```bash
# Terminal 3: Start the Flask demo app
python app_integration_example.py
# Then open: http://localhost:5000
```

## 📋 API Endpoints

### Health Check
```bash
GET http://localhost:8080/health
```

### Create Session
```bash
POST http://localhost:8080/sessions
Content-Type: application/json

{
    "user_id": "user123",
    "app_name": "overlay_generator"
}
```

### Generate JavaScript
```bash
POST http://localhost:8080/run
Content-Type: application/json

{
    "message": "change bg to red",
    "user_id": "user123",
    "session_id": "your_session_id"
}
```

## 🔧 Integration Examples

### Python Integration
```python
from adk_client import ADKClient

# Initialize client
client = ADKClient("http://localhost:8080")

# Generate JavaScript
result = client.generate_overlay_js("change bg to red")

if result["success"]:
    js_code = result["javascript"]
    print(f"Generated JS: {js_code}")
else:
    print(f"Error: {result['error']}")
```

### JavaScript/Node.js Integration
```javascript
async function generateOverlay(prompt) {
    // Create session
    const sessionResponse = await fetch('http://localhost:8080/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: 'user123',
            app_name: 'overlay_generator'
        })
    });
    const sessionData = await sessionResponse.json();
    
    // Generate JavaScript
    const response = await fetch('http://localhost:8080/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: prompt,
            user_id: 'user123',
            session_id: sessionData.session_id
        })
    });
    
    const result = await response.json();
    return result.response; // Raw JavaScript code
}

// Usage
const jsCode = await generateOverlay("change bg to red");
```

### cURL Integration
```bash
# 1. Create session
SESSION_ID=$(curl -s -X POST "http://localhost:8080/sessions" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "app_name": "overlay_generator"}' \
  | jq -r '.session_id')

# 2. Generate JavaScript
curl -X POST "http://localhost:8080/run" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "change bg to red",
    "user_id": "user123",
    "session_id": "'$SESSION_ID'"
  }'
```

## 🎯 Usage Examples

### Common Prompts
- `"change bg to red"` - Changes background to red
- `"create an overlay"` - Creates Apple-style glass overlay
- `"add a note"` - Adds floating note overlay
- `"change background to blue"` - Changes background to blue

### Response Format
```json
{
    "success": true,
    "javascript": "// Change background to red\n(function() \n{\n    document.body.style.backgroundColor = 'red';\n    console.log('Background changed to red');\n})();",
    "session_id": "session_123",
    "raw_response": {...}
}
```

## ⚠️ Important Notes

1. **Session Management**: Each API call requires a session. Create one per user session.

2. **Error Handling**: Always check the `success` field in responses.

3. **Raw JavaScript**: The agent returns raw JavaScript code that can be directly executed.

4. **CORS**: If calling from a browser, you may need to configure CORS.

5. **Security**: In production, add authentication and rate limiting.

## 🔧 Troubleshooting

### Common Issues

**Connection refused**: Make sure ADK server is running on port 8080
```bash
adk api_server overlay_agent_dir --port 8080
```

**Session not found**: Create a new session before making requests

**No response**: Check if the agent is properly configured and the tool is working

**JavaScript not working**: Ensure the generated code is valid and doesn't conflict with CSP policies

### Debug Mode
Add debug logging to see what's happening:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📱 Production Deployment

For production use:
1. Deploy ADK server using `adk deploy` to Google Cloud
2. Update client URLs to production endpoints
3. Add authentication and rate limiting
4. Monitor API performance and errors
5. Set up proper logging and monitoring

## 🎉 Next Steps

1. Customize the JavaScript generation logic in `overlay_agent.py`
2. Add more overlay types and functionality
3. Implement user authentication
4. Add caching for better performance
5. Create a proper web interface for your users 