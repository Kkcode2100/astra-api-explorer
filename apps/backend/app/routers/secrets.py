from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db import get_session
from app.models import Secret
from app.security import encrypt_str

router = APIRouter()


class SetHeaderBody(BaseModel):
	header: str
	value: str


@router.get("/envs")
async def list_envs(session: Session = Depends(get_session)) -> Dict[str, List[str]]:
	items = session.exec(select(Secret)).all()
	envs: Dict[str, List[str]] = {}
	for s in items:
		if not s.name.startswith("env::"):
			continue
		parts = s.name.split("::")
		if len(parts) >= 4 and parts[2] == "header":
			env = parts[1]
			h = parts[3]
			envs.setdefault(env, []).append(h)
	return envs


@router.get("/envs/{env}")
async def get_env(env: str, session: Session = Depends(get_session)) -> Dict[str, List[str]]:
	items = session.exec(select(Secret).where(Secret.name.like(f"env::{env}::header::%"))).all()
	headers = []
	for s in items:
		parts = s.name.split("::")
		if len(parts) == 4:
			headers.append(parts[3])
	return {"env": env, "headers": headers}


@router.post("/envs/{env}/set-header")
async def set_env_header(env: str, body: SetHeaderBody, session: Session = Depends(get_session)) -> Dict[str, Any]:
	name = f"env::{env}::header::{body.header}"
	secret = session.exec(select(Secret).where(Secret.name == name)).first()
	enc = encrypt_str(body.value)
	if secret:
		secret.value_encrypted = enc
	else:
		secret = Secret(name=name, value_encrypted=enc)
		session.add(secret)
	session.commit()
	return {"ok": True}