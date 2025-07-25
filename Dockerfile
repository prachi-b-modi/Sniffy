FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent code
COPY overlay_agent_dir/ ./overlay_agent_dir/
COPY .env .env

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV GOOGLE_GENAI_USE_VERTEXAI=false

# Expose port
EXPOSE ${PORT}

# Run the ADK API server
CMD ["python", "-m", "google.adk.cli.main", "api_server", "overlay_agent_dir", "--port", "8080", "--host", "0.0.0.0"] 