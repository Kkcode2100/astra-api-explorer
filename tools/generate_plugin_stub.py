#!/usr/bin/env python3
import io
import os
import zipfile

VERSION = os.environ.get("MORPHEUS_PLUGIN_API_VERSION", "1.2.8")
if VERSION not in {"1.2.8", "1.2.9"}:
	VERSION = "1.2.8"

os.makedirs("artifacts", exist_ok=True)
path = os.path.join("artifacts", "morpheus-plugin-stub.zip")
with zipfile.ZipFile(path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
	zf.writestr("README.md", f"""# Morpheus Plugin Stub\n\nBuild with Gradle.\n\n- morpheus-plugin-api: {VERSION}\n- Java 11+\n\nRun:\n\n```bash\n./gradlew build\n```\n""")
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
	implementation 'com.morpheusdata:morpheus-plugin-api:{VERSION}'
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

print(f"Wrote {path}")