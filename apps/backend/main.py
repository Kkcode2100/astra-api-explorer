import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.db import init_db
from app.config import settings
from app.routers import health, specs, requests as reqs, morpheus, codegen
from app.routers import secrets as secrets_router


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request: Request, call_next):
		response: Response = await call_next(request)
		response.headers["X-Content-Type-Options"] = "nosniff"
		response.headers["X-Frame-Options"] = "DENY"
		response.headers["X-XSS-Protection"] = "0"
		response.headers["Referrer-Policy"] = "no-referrer"
		response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:; connect-src *; img-src * data: blob:;"
		return response


app = FastAPI(title="Astra API", version="0.1.0")

# CORS
origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins or ["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)


@app.on_event("startup")
async def on_startup() -> None:
	init_db()


# Routers
app.include_router(health.router)
app.include_router(specs.router, prefix="/specs", tags=["specs"])
app.include_router(reqs.router, prefix="/requests", tags=["requests"])
app.include_router(morpheus.router, prefix="/morpheus", tags=["morpheus"])
app.include_router(codegen.router, prefix="/codegen", tags=["codegen"])
app.include_router(secrets_router.router, prefix="/secrets", tags=["secrets"])