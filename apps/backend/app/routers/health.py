from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict:
	return {"status": "ok"}


@router.get("/version")
async def version() -> dict:
	return {"name": "astra", "version": "0.1.0"}