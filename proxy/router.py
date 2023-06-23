import re

import httpx
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from utils.logger import logger
from settings import settings

app = FastAPI()


@app.get("/{path:path}")
async def proxy(path: str):
    url = f"{settings.base_url}/{path}"

    try:
        logger.debug("Sending request to %s", url)  # record the log before sending the request
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if 200 <= response.status_code < 400:
                modified_content = re.sub(r"Black(\s*<[^>]+>)?\s*Russia", "BlackHub Games", response.text,
                                          flags=re.IGNORECASE)
                return modified_content

            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="Not found")

    except httpx.RequestError as exc:
        logger.error(f"Request error: {str(exc)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTPException: {exc.status_code} - {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.route("/{path:path}", methods=["POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def handle_other_methods(path: str):
    raise HTTPException(status_code=405, detail="Method Not Allowed")
