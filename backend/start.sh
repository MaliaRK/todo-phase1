#!/bin/sh
# Start the FastAPI application with the PORT environment variable
PORT=${PORT:-8000}
exec uvicorn src.main:app --host 0.0.0.0 --port $PORT