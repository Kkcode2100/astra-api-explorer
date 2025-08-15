from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.db import get_session
from app.models import SavedRequest
from app.security import redact

router = APIRouter()


class SendRequestBody(BaseModel):
	method: str = Field(..., description="HTTP method")
	url: str
	headers: Dict[str, str] = {}
	params: Dict[str, Any] = {}
	body: Optional[str] = None
	save_as: Optional[str] = None


@router.post("/send")
async def send_request(payload: SendRequestBody, session: Session = Depends(get_session)) -> dict:
	try:
		async with httpx.AsyncClient(timeout=30.0) as client:
			request_args = {
				"method": payload.method.upper(),
				"url": payload.url,
				"headers": payload.headers or {},
				"params": payload.params or {},
			}
			if payload.body:
				request_args["content"] = payload.body
			resp = await client.request(**request_args)
		except httpx.RequestError as exc:
			raise HTTPException(status_code=400, detail=f"Request failed: {exc}")

	if payload.save_as:
		item = SavedRequest(
			name=payload.save_as,
			method=payload.method.upper(),
			url=payload.url,
			headers_json=json.dumps(payload.headers or {}),
			params_json=json.dumps(payload.params or {}),
			body=payload.body,
		)
		session.add(item)
		session.commit()
		session.refresh(item)

	return {
		"status": resp.status_code,
		"headers": dict(resp.headers),
		"body": resp.text,
	}


@router.get("")
async def list_saved_requests(session: Session = Depends(get_session)) -> List[SavedRequest]:
	return session.exec(select(SavedRequest)).all()