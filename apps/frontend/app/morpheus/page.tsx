"use client";

import { useEffect, useState } from "react";
import axios from "axios";

const API = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

type ServicePlan = { id?: number; name?: string; description?: string };

export default function MorpheusServicePlansPage() {
	const [items, setItems] = useState<ServicePlan[]>([]);
	const [page, setPage] = useState(0);
	const [max, setMax] = useState(25);
	const [error, setError] = useState<string | null>(null);

	async function load() {
		try {
			const res = await axios.get(`${API}/morpheus/service-plans/discover`, { params: { page, max } });
			setItems(res.data.items || []);
			setError(null);
		} catch (e: any) {
			setError(e?.response?.data?.detail || e?.message || "Unknown error");
		}
	}

	useEffect(() => {
		load();
	}, [page, max]);

	return (
		<div style={{ padding: 16 }}>
			<h3>Morpheus: Service Plans</h3>
			<div style={{ display: "flex", gap: 8, alignItems: "center" }}>
				<button onClick={() => setPage(Math.max(0, page - 1))} disabled={page <= 0}>Prev</button>
				<span>Page: {page}</span>
				<button onClick={() => setPage(page + 1)}>Next</button>
				<select value={max} onChange={e => setMax(parseInt(e.target.value))}>
					<option value={25}>25</option>
					<option value={50}>50</option>
					<option value={100}>100</option>
				</select>
			</div>
			{error ? <div style={{ color: 'red' }}>Error: {error}</div> : null}
			<table style={{ width: '100%', marginTop: 12, borderCollapse: 'collapse' }}>
				<thead>
					<tr>
						<th style={{ textAlign: 'left', borderBottom: '1px solid #ddd' }}>Name</th>
						<th style={{ textAlign: 'left', borderBottom: '1px solid #ddd' }}>Description</th>
					</tr>
				</thead>
				<tbody>
					{items.map((sp, i) => (
						<tr key={i}>
							<td style={{ padding: '4px 8px' }}>{sp.name || '-'}</td>
							<td style={{ padding: '4px 8px' }}>{sp.description || '-'}</td>
						</tr>
					))}
				</tbody>
			</table>
		</div>
	);
}