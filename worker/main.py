import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from config.routes import setup_routes

import json_log_formatter
import logging
import sys
from datetime import datetime
import httpx
import time

# Set up logging
logLevel = os.getenv("LOG_LEVEL", "INFO").upper()
formatter = json_log_formatter.VerboseJSONFormatter()
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(getattr(logging, logLevel))

# Configure the root logger
logging.basicConfig(
    handlers=[stdout_handler], 
    level=getattr(logging, logLevel)
    # format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s"
)

# Apply the same handler to uvicorn loggers explicitly
for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
    uv_logger = logging.getLogger(logger_name)
    uv_logger.handlers = [stdout_handler]
    uv_logger.propagate = False
    uv_logger.setLevel(getattr(logging, logLevel))

# Your app logger
logger = logging.getLogger(__name__)

# App Details
app_title = "Worker Process"
app_version = "1.0.0"
app_description = "A Worker Process."

app = FastAPI(title=app_title, version=app_version, description=app_description)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup routes using the centralized configuration
setup_routes(app)

@app.get("/")
async def root():
    return {"message": "Worker process is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("main:app", host="0.0.0.0", port=int(settings.port), reload=True)
