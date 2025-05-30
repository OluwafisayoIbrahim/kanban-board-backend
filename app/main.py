from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS 
from app.routers.auth import router as auth_router
from app.db.base import init_db
from app.dependencies import verify_api_key
from app.routers.auth import router as auth_router
from fastapi.openapi.utils import get_openapi

init_db()

app = FastAPI(
    title="FlowSpace API",  
    description="REST API for FlowSpace Kanban Board",        
    version="0.1.0"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FlowSpace API",
        version="1.0.0",
        description="REST API for FlowSpace Kanban Board",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # apply globally, or you can apply per-route via `security=[...]`
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
