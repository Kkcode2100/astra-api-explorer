from __future__ import annotations

from typing import Any, Dict, List


def list_endpoints(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
	paths = spec.get("paths", {}) or {}
	servers = spec.get("servers", []) or []
	base_url = None
	if servers and isinstance(servers, list):
		first = servers[0] or {}
		base_url = first.get("url")
	endpoints: List[Dict[str, Any]] = []
	for path, path_item in paths.items():
		if not isinstance(path_item, dict):
			continue
		for method in ["get", "post", "put", "patch", "delete", "head", "options"]:
			op = path_item.get(method)
			if not isinstance(op, dict):
				continue
			tags = op.get("tags", [])
			summary = op.get("summary") or op.get("operationId") or f"{method.upper()} {path}"
			endpoints.append({
				"method": method.upper(),
				"path": path,
				"summary": summary,
				"operationId": op.get("operationId"),
				"tags": tags,
				"baseUrl": base_url,
			})
	return endpoints