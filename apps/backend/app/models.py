from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class ApiSpec(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	type: str = Field(description="openapi|postman|asyncapi")
	raw: str = Field(description="Raw JSON/YAML string of the spec")
	created_at: datetime = Field(default_factory=datetime.utcnow)


class SavedRequest(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	method: str
	url: str
	headers_json: str = Field(default="{}")
	params_json: str = Field(default="{}")
	body: Optional[str] = None
	spec_id: Optional[int] = Field(default=None, foreign_key="apispec.id")
	created_at: datetime = Field(default_factory=datetime.utcnow)


class AuditEvent(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	timestamp: datetime = Field(default_factory=datetime.utcnow)
	actor: str = Field(default="system")
	action: str
	target: str
	context_json: str = Field(default="{}")


class Secret(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str = Field(unique=True, index=True)
	value_encrypted: str
	created_at: datetime = Field(default_factory=datetime.utcnow)