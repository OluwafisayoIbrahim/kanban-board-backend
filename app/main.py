from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import asyncio

from app.core.config import CORS_ORIGINS
from app.db.base import init_db
from app.routers.auth import router as auth_router
from app.routers.profile import router as profile_router

init_db()

app = FastAPI(
    title="FlowSpace API",
    description="REST API for FlowSpace Kanban Board.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,     
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],            
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(profile_router, prefix="/api/profile", tags=["profile"])

@app.get("/", include_in_schema=False)
async def root():
    return {"status": "ok"}

async def cleanup_expired_tokens_task():
    """Background task to clean up expired tokens"""
    while True:
        try:
            from app.db.crud import cleanup_expired_tokens
            cleanup_expired_tokens()
            print("Cleaned up expired tokens")
        except Exception as e:
            print(f"Error in cleanup task: {e}")
        
        await asyncio.sleep(3600)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_expired_tokens_task())

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title="FlowSpace API",
        version="1.0.0",
        description="REST API for FlowSpace Kanban Board",
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi