from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Proxy Black Russia API")


@router.get("/openapi.json")
async def get_openapi_endpoint():
    return get_openapi(title="Proxy Black Russia API", version="0.1", routes=router.routes)
