from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
async def healthz() -> dict:
	return {"status": "ok"}


@router.get("/version")
async def version() -> dict:
	return {"name": "astra", "version": "0.1.0"}