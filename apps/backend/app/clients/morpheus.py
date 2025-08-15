from __future__ import annotations

from typing import Any, Dict, List

import httpx

from app.config import settings


class MorpheusClient:
	def __init__(self, base_url: str | None = None, token: str | None = None) -> None:
		self.base_url = (base_url or settings.MORPHEUS_URL).rstrip('/')
		self.token = token or settings.MORPHEUS_TOKEN
		self._client = httpx.AsyncClient(base_url=self.base_url, headers={
			"Authorization": f"Bearer {self.token}",
			"Accept": "application/json",
		})

	async def close(self) -> None:
		await self._client.aclose()

	async def list_service_plans(self, page: int = 0, max: int = 100) -> List[Dict[str, Any]]:
		resp = await self._client.get(f"/api/service-plans", params={"page": page, "max": max})
		resp.raise_for_status()
		data = resp.json()
		# Morpheus returns { servicePlans: [...], meta: {...} }
		return data.get("servicePlans", [])

	async def diff_service_plans(self, desired: List[Dict[str, Any]]) -> Dict[str, Any]:
		# TODO: Official payload docs
		current = await self.list_service_plans()
		# Simple name-index compare for MVP
		curr_by_name = {sp.get("name"): sp for sp in current}
		plan = {"create": [], "update": [], "noop": []}
		for d in desired:
			name = d.get("name")
			if name not in curr_by_name:
				plan["create"].append(d)
			else:
				plan["noop"].append(name)
		return plan

	async def apply_service_plans(self, plan: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
		# For MVP, return the plan if dry_run, otherwise simulate success
		if dry_run:
			return {"applied": False, "plan": plan}
		# TODO: Implement POST/PUT calls to create/update service plans based on Morpheus API
		return {"applied": True, "created": len(plan.get("create", [])), "updated": len(plan.get("update", []))}