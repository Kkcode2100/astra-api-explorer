"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";

const API = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

type Spec = { id: number; name: string };

type Endpoint = { method: string; path: string; summary?: string; baseUrl?: string };

export default function HomePage() {
	const [specs, setSpecs] = useState<Spec[]>([]);
	const [url, setUrl] = useState("");
	const [selectedSpecId, setSelectedSpecId] = useState<number | null>(null);
	const [endpoints, setEndpoints] = useState<Endpoint[]>([]);
	const [selectedEndpoint, setSelectedEndpoint] = useState<Endpoint | null>(null);
	const [response, setResponse] = useState<any>(null);
	const [saveName, setSaveName] = useState("");
	const [env, setEnv] = useState("default");
	const [apiKeyHeaderName, setApiKeyHeaderName] = useState("x-api-key");
	const [apiKeyValue, setApiKeyValue] = useState("");

	async function refreshSpecs() {
		const res = await axios.get(`${API}/specs`);
		setSpecs(res.data);
	}

	useEffect(() => {
		refreshSpecs();
	}, []);

	async function importUrl() {
		if (!url) return;
		await axios.post(`${API}/specs/import/url`, new URLSearchParams({ url }));
		setUrl("");
		await refreshSpecs();
	}

	async function loadEndpoints(id: number) {
		setSelectedSpecId(id);
		const res = await axios.get(`${API}/specs/${id}/endpoints`);
		setEndpoints(res.data.endpoints);
	}

	async function saveEnvHeader() {
		if (!apiKeyValue) return;
		await axios.post(`${API}/secrets/envs/${env}/set-header`, { header: apiKeyHeaderName, value: apiKeyValue });
		setApiKeyValue("");
	}

	async function runGet() {
		if (!selectedEndpoint) return;
		const fullUrl = selectedEndpoint.path.startsWith("http")
			? selectedEndpoint.path
			: `${selectedEndpoint.baseUrl || ""}${selectedEndpoint.path}`;
		const res = await axios.post(`${API}/requests/send`, {
			method: selectedEndpoint.method,
			url: fullUrl,
			headers: {},
			params: {},
			body: undefined,
			save_as: saveName || undefined,
			env,
		});
		setResponse(res.data);
	}

	return (
		<div style={{ padding: 16, display: "grid", gridTemplateColumns: "320px 1fr", gap: 16 }}>
			<div>
				<h3>API Explorer</h3>
				<div style={{ display: "flex", gap: 8 }}>
					<input placeholder="OpenAPI URL" value={url} onChange={e => setUrl(e.target.value)} style={{ flex: 1 }} />
					<button onClick={importUrl}>Import</button>
				</div>
				<div style={{ marginTop: 12 }}>
					<label>Environment:</label>
					<select value={env} onChange={e => setEnv(e.target.value)}>
						<option value="default">default</option>
						<option value="prod">prod</option>
						<option value="dev">dev</option>
					</select>
					<div style={{ display: "flex", gap: 8, marginTop: 8 }}>
						<input placeholder="API key header (e.g. x-api-key, Authorization)" value={apiKeyHeaderName} onChange={e => setApiKeyHeaderName(e.target.value)} />
						<input placeholder="Secret value" value={apiKeyValue} onChange={e => setApiKeyValue(e.target.value)} />
						<button onClick={saveEnvHeader}>Save</button>
					</div>
				</div>
				<ul>
					{specs.map(s => (
						<li key={s.id}>
							<button onClick={() => loadEndpoints(s.id)}>{s.name}</button>
						</li>
					))}
				</ul>
				<hr />
				<h4>Endpoints</h4>
				<ul>
					{endpoints.map((ep, i) => (
						<li key={i}>
							<button onClick={() => setSelectedEndpoint(ep)}>
								{ep.method} {ep.path} {ep.summary ? `- ${ep.summary}` : ""}
							</button>
						</li>
					))}
				</ul>
			</div>
			<div>
				<div style={{ display: 'flex', gap: 12, marginBottom: 8 }}>
					<Link href="/api-explorer">API Explorer</Link>
					<Link href="/morpheus">Morpheus</Link>
				</div>
				<h3>Request Builder</h3>
				<div>
					<div>Selected: {selectedEndpoint ? `${selectedEndpoint.method} ${selectedEndpoint.path}` : "None"}</div>
					<input placeholder="Save as" value={saveName} onChange={e => setSaveName(e.target.value)} />
					<button onClick={runGet} disabled={!selectedEndpoint}>Send</button>
				</div>
				<div style={{ marginTop: 16 }}>
					<h4>Response</h4>
					<pre style={{ whiteSpace: 'pre-wrap' }}>{response ? JSON.stringify(response, null, 2) : ""}</pre>
				</div>
			</div>
		</div>
	);
}