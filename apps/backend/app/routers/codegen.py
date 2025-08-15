from __future__ import annotations

import io
import os
import zipfile
from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/morpheus-plugin-stub.zip")
async def generate_morpheus_plugin_stub(payload: Dict[str, Any] | None = None):
	version = (payload or {}).get("pluginApiVersion", "1.2.8")
	if version not in {"1.2.8", "1.2.9"}:
		version = "1.2.8"
	mem = io.BytesIO()
	with zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
		zf.writestr("README.md", f"""# Morpheus Plugin Stub\n\nBuild with Gradle.\n\n- morpheus-plugin-api: {version}\n- Java 11+\n\n```bash\n./gradlew build\n```\n""")
		zf.writestr("build.gradle", f"""
plugins {{
	id 'java'
}}

group = 'com.example'
version = '0.1.0'

repositories {{
	mavenCentral()
}}

dependencies {{
	implementation 'com.morpheusdata:morpheus-plugin-api:{version}'
	testImplementation 'junit:junit:4.13.2'
}}

sourceCompatibility = JavaVersion.VERSION_11

""")
		zf.writestr("settings.gradle", "rootProject.name = 'morpheus-plugin-stub'\n")
		zf.writestr("src/main/java/com/example/ExamplePlugin.java", """
package com.example;

import com.morpheusdata.core.Plugin;

public class ExamplePlugin extends Plugin {
	public ExamplePlugin() {
		this.setName("Example Morpheus Plugin");
	}
}
""")
	mem.seek(0)
	return StreamingResponse(mem, media_type="application/zip", headers={
		"Content-Disposition": "attachment; filename=morpheus-plugin-stub.zip"
	})