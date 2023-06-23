import re
from itertools import chain

from fastapi import FastAPI, HTTPException
import httpx
from starlette.responses import JSONResponse

from proxy.logger import logger

app = FastAPI()

STATUS_200_LIST = range(200, 300)
STATUS_300_LIST = range(300, 400)
STATUS_OK_LIST = list(chain(STATUS_200_LIST, STATUS_300_LIST))


@app.get("/{path:path}")
async def proxy(path: str):
    url = f"https://blackrussia.online/{path}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code in STATUS_OK_LIST:
                modified_content = re.sub(r"Black(\s*<[^>]+>)?\s*Russia", "BlackHub Games", response.text,
                                          flags=re.IGNORECASE)
                return modified_content

            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Not found")

    except httpx.RequestError as exc:
        logger.error(f"Request error: {str(exc)}")
        raise HTTPException(status_code=502, detail="Bad Gateway") from exc

    logger.error(f"Unknown error occurred")
    raise HTTPException(status_code=500, detail="Unknown error")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.route("/{path:path}", methods=["POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def handle_other_methods(path: str):
    raise HTTPException(status_code=405, detail="Method Not Allowed")
