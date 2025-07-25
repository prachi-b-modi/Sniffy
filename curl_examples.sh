#!/bin/bash

# cURL examples for testing the ADK overlay agent API server
# Make sure your ADK server is running: adk api_server overlay_agent_dir --port 8080

echo "🏥 Testing ADK API Server Health Check"
echo "======================================"

# Health check
curl -X GET "http://localhost:8080/health" \
  -H "Content-Type: application/json" \
  -w "\nStatus: %{http_code}\n\n"

echo "📝 Creating a session"
echo "===================="

# Create session and capture session_id
SESSION_RESPONSE=$(curl -s -X POST "http://localhost:8080/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "app_name": "overlay_generator"
  }')

echo "Session Response: $SESSION_RESPONSE"

# Extract session_id (assuming jq is installed)
SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

echo -e "\n🚀 Testing overlay generation requests"
echo "======================================"

# Test 1: Change background to red
echo "Test 1: Change background to red"
curl -X POST "http://localhost:8080/run" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "change bg to red",
    "user_id": "user123",
    "session_id": "'$SESSION_ID'"
  }' \
  -w "\nStatus: %{http_code}\n\n"

# Test 2: Create an overlay
echo "Test 2: Create an overlay"
curl -X POST "http://localhost:8080/run" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "create an overlay",
    "user_id": "user123",
    "session_id": "'$SESSION_ID'"
  }' \
  -w "\nStatus: %{http_code}\n\n"

# Test 3: Add a note
echo "Test 3: Add a note"
curl -X POST "http://localhost:8080/run" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "add a note",
    "user_id": "user123",
    "session_id": "'$SESSION_ID'"
  }' \
  -w "\nStatus: %{http_code}\n\n"

# Test 4: Change background to blue
echo "Test 4: Change background to blue"
curl -X POST "http://localhost:8080/run" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "change background to blue",
    "user_id": "user123",
    "session_id": "'$SESSION_ID'"
  }' \
  -w "\nStatus: %{http_code}\n\n"

echo "✅ All tests completed!"
echo "Note: If you don't have jq installed, you'll need to manually extract the session_id from the session response." 