from __future__ import annotations

import json
from typing import Any
from cryptography.fernet import Fernet
from app.config import settings


def get_fernet() -> Fernet:
	return Fernet(settings.fernet_key())


def encrypt_str(value: str) -> str:
	return get_fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_str(token: str) -> str:
	return get_fernet().decrypt(token.encode("utf-8")).decode("utf-8")


def redact(obj: Any) -> Any:
	try:
		data = json.loads(obj) if isinstance(obj, str) else obj
		def _walk(x):
			if isinstance(x, dict):
				return {k: ("***" if k.lower() in {"authorization", "token", "password", "secret"} else _walk(v)) for k, v in x.items()}
			if isinstance(x, list):
				return [_walk(v) for v in x]
			return x
		return _walk(data)
	except Exception:
		return "<redacted>"