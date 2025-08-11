from fastapi import APIRouter, HTTPException, Response
import logging
import httpx

router = APIRouter()
logger = logging.getLogger(__name__)

LB_URL = "http://lb:5000"
AFFINITY_HEADER = "X-Session-Affinity"
WORKER_HEADER = "X-Worker-Id"

# Store affinity ID in memory (per api-server instance)
affinity_id = None

@router.get("/some_request")
async def some_request(response: Response):
    global affinity_id

    logger.info("Received request for /some_request")

    try:
        headers = {}
        if affinity_id:
            headers[AFFINITY_HEADER] = affinity_id
            logger.info(f"Using stored session affinity: {affinity_id}")
        else:
            logger.info("No session affinity yet, will round robin via LB")

        async with httpx.AsyncClient() as client:
            r = await client.get(f"{LB_URL}/api/requests/some_worker_request", headers=headers)
            r.raise_for_status()

        # Save affinity header if present (so future calls stick to same worker)
        if AFFINITY_HEADER in r.headers:
            affinity_id = r.headers[AFFINITY_HEADER]
            logger.info(f"Updated session affinity to: {affinity_id}")

        # Forward important headers (including worker id) to the caller
        for header in ["X-Backend", "X-Backend-IP", AFFINITY_HEADER, WORKER_HEADER]:
            if header in r.headers:
                response.headers[header] = r.headers[header]

        return r.json()

    except Exception as e:
        logger.error(f"Error doing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
