from __future__ import annotations

import os
from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

_engine = None


def get_engine():
	global _engine
	if _engine is None:
		db_url = settings.DATABASE_URL
		if db_url.startswith("sqlite"):
			# Ensure directory
			os.makedirs("data", exist_ok=True)
			connect_args = {"check_same_thread": False}
			_engine = create_engine(db_url, echo=False, connect_args=connect_args)
		else:
			_engine = create_engine(db_url, echo=False)
	return _engine


def init_db() -> None:
	engine = get_engine()
	from app import models  # noqa: F401 ensure models are registered
	SQLModel.metadata.create_all(engine)


def get_session() -> Session:
	engine = get_engine()
	with Session(engine) as session:
		yield session