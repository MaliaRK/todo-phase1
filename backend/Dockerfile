# Base Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Expose port (Railway uses this, but CMD handles dynamic PORT)
EXPOSE 8080

# Start the app
CMD sh -c "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}"

