#!/usr/bin/env python3
"""
Entry point script for Railway deployment
"""
import os
import sys
import uvicorn
from src.main import app

def main():
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()