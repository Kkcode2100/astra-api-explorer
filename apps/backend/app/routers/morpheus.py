from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query

from app.clients.morpheus import MorpheusClient

router = APIRouter()


@router.get("/service-plans/discover")
async def discover_service_plans(page: int = Query(0, ge=0), max: int = Query(100, ge=1, le=500)) -> Dict[str, Any]:
	client = MorpheusClient()
	try:
		plans = await client.list_service_plans(page=page, max=max)
	finally:
		await client.close()
	return {"items": plans}


@router.post("/service-plans/diff")
async def diff_service_plans(desired: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
	client = MorpheusClient()
	try:
		plan = await client.diff_service_plans(desired.get("items", []))
	finally:
		await client.close()
	return {"plan": plan}


@router.post("/service-plans/apply")
async def apply_service_plans(payload: Dict[str, Any]) -> Dict[str, Any]:
	plan = payload.get("plan", {})
	dry_run = bool(payload.get("dryRun", True))
	client = MorpheusClient()
	try:
		result = await client.apply_service_plans(plan, dry_run=dry_run)
	finally:
		await client.close()
	return result