from __future__ import annotations

import base64
import hashlib
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False)

	ENVIRONMENT: str = "development"
	ALLOWED_ORIGINS: str = "http://localhost:3000"
	DATABASE_URL: str = "sqlite:///data/astra.db"
	SECRET_KEY: str = "dev-secret-change-me"

	MORPHEUS_URL: str = ""
	MORPHEUS_TOKEN: str = ""

	REDIS_URL: str = "redis://redis:6379/0"
	APPLY_ENABLED: bool = False

	def fernet_key(self) -> bytes:
		# Derive a stable fernet key from SECRET_KEY
		sha = hashlib.sha256(self.SECRET_KEY.encode("utf-8")).digest()
		return base64.urlsafe_b64encode(sha)


settings = Settings()