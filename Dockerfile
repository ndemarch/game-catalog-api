# Use a minimal Python image
FROM python:3.11-slim

# Set workdir in the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app ./app
COPY tests ./tests

# Expose the API port
EXPOSE 8000

# Default command: run the FastAPI app (overridden in docker-compose when needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

