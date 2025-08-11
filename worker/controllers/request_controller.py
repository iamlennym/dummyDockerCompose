from fastapi import APIRouter, HTTPException, Response
import logging
import os
import socket

router = APIRouter()
logger = logging.getLogger(__name__)

worker_id = os.getenv("WORKER_NAME", socket.gethostname())

@router.get("/some_worker_request")
async def some_worker_request(response: Response):
    try:
        response.headers["X-Worker-Id"] = worker_id
        return {
            "message": "Request invoked successfully",
            "worker_id": worker_id
        }
    except Exception as e:
        logger.error(f"Error doing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
