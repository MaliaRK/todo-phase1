#!/usr/bin/env python3
"""
Custom startup script for the backend to handle initialization properly.
"""

import os
import sys

# Clear any proxy settings that might interfere with OpenAI client before any imports
proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
for var in proxy_vars:
    if var in os.environ:
        print(f"Removing environment variable: {var}", file=sys.stderr)
        del os.environ[var]

# Now import and run the application
from uvicorn import Config, Server
from src.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    config = Config(app, host=host, port=port, reload=False)
    server = Server(config)

    import asyncio
    asyncio.run(server.serve())