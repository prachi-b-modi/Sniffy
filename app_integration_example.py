#!/usr/bin/env python3
"""
Example Flask app showing how to integrate the ADK overlay agent
"""

from flask import Flask, request, jsonify, render_template_string
from adk_client import ADKClient
import json

app = Flask(__name__)

# Initialize ADK client
adk_client = ADKClient("http://localhost:8080")

# Simple HTML template for testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ADK Overlay Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .form-group { margin-bottom: 20px; }
        input, textarea { width: 100%; padding: 10px; margin-top: 5px; }
        button { background: #007AFF; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
        .error { background: #f8d7da; color: #721c24; }
        .success { background: #d4edda; color: #155724; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 ADK Overlay Generator</h1>
        <p>Generate JavaScript code for website overlays using natural language.</p>
        
        <form onsubmit="generateOverlay(event)">
            <div class="form-group">
                <label>What would you like to do?</label>
                <input type="text" id="prompt" placeholder="e.g., change bg to red, create an overlay, add a note" required>
            </div>
            <button type="submit">Generate JavaScript</button>
        </form>
        
        <div id="result" style="display: none;"></div>
    </div>

    <script>
        async function generateOverlay(event) {
            event.preventDefault();
            
            const prompt = document.getElementById('prompt').value;
            const resultDiv = document.getElementById('result');
            
            // Show loading
            resultDiv.innerHTML = '<div class="result">⏳ Generating JavaScript...</div>';
            resultDiv.style.display = 'block';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt: prompt })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultDiv.innerHTML = `
                        <div class="result success">
                            <h3>✅ JavaScript Generated Successfully!</h3>
                            <p><strong>Prompt:</strong> ${prompt}</p>
                            <p><strong>Instructions:</strong> Copy the code below and paste it into your browser's developer console (F12).</p>
                            <pre>${data.javascript}</pre>
                            <button onclick="copyToClipboard()">📋 Copy to Clipboard</button>
                        </div>
                    `;
                    window.generatedJs = data.javascript;
                } else {
                    resultDiv.innerHTML = `
                        <div class="result error">
                            <h3>❌ Error</h3>
                            <p>${data.error}</p>
                        </div>
                    `;
                }
            } catch (error) {
                resultDiv.innerHTML = `
                    <div class="result error">
                        <h3>❌ Connection Error</h3>
                        <p>Failed to connect to the ADK server. Make sure it's running on localhost:8080</p>
                        <p>Error: ${error.message}</p>
                    </div>
                `;
            }
        }
        
        function copyToClipboard() {
            navigator.clipboard.writeText(window.generatedJs).then(() => {
                alert('JavaScript code copied to clipboard!');
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    """Generate JavaScript code from prompt"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'No prompt provided'
            }), 400
        
        # Generate JavaScript using ADK client
        result = adk_client.generate_overlay_js(prompt)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/health')
def health():
    """Check health of both this app and the ADK server"""
    adk_health = adk_client.health_check()
    
    return jsonify({
        'app_status': 'healthy',
        'adk_server_status': adk_health['status'],
        'adk_server_details': adk_health
    })

if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    print("📋 Make sure your ADK server is running:")
    print("   adk api_server overlay_agent_dir --port 8080")
    print("🌐 App will be available at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 