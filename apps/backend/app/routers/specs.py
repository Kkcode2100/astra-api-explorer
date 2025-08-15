from __future__ import annotations

import json
from typing import List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session, select

from app.db import get_session
from app.models import ApiSpec
from app.utils.openapi_parser import list_endpoints

router = APIRouter()


@router.get("")
async def list_specs(session: Session = Depends(get_session)) -> List[ApiSpec]:
	return session.exec(select(ApiSpec)).all()


@router.post("/import/url")
async def import_spec_url(url: str = Form(...), session: Session = Depends(get_session)) -> dict:
	try:
		async with httpx.AsyncClient(timeout=20) as client:
			resp = await client.get(url)
			resp.raise_for_status()
			raw_text = resp.text
	except Exception as exc:
		raise HTTPException(status_code=400, detail=f"Failed to fetch spec: {exc}")
	item = ApiSpec(name=url.split("/")[-1] or "spec", type="openapi", raw=raw_text)
	session.add(item)
	session.commit()
	session.refresh(item)
	return {"id": item.id}


@router.post("/import/file")
async def import_spec_file(file: UploadFile = File(...), session: Session = Depends(get_session)) -> dict:
	raw_text = (await file.read()).decode("utf-8")
	item = ApiSpec(name=file.filename, type="openapi", raw=raw_text)
	session.add(item)
	session.commit()
	session.refresh(item)
	return {"id": item.id}


@router.get("/{spec_id}/endpoints")
async def get_spec_endpoints(spec_id: int, session: Session = Depends(get_session)) -> dict:
	spec = session.get(ApiSpec, spec_id)
	if not spec:
		raise HTTPException(status_code=404, detail="Spec not found")
	try:
		parsed = json.loads(spec.raw)
	except Exception:
		raise HTTPException(status_code=400, detail="Spec content must be JSON for MVP")
	endpoints = list_endpoints(parsed)
	return {"endpoints": endpoints}