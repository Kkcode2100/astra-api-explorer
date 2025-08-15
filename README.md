# Astra - API Explorer & Integration Builder

## Quickstart (Docker)

1. Copy backend env: `cp apps/backend/.env.example apps/backend/.env` and set values if needed.
2. Build & run: `docker compose up --build`
3. UI: http://localhost:3000, API: http://localhost:8000

## Local Dev

- Backend: `uvicorn apps.backend.main:app --reload` (from repo root, set `PYTHONPATH=apps/backend`)
- Frontend: `pnpm -C apps/frontend dev`

## Minimal Flow (M1)

- Import OpenAPI URL (e.g. Petstore `https://petstore3.swagger.io/api/v3/openapi.json`)
- Browse endpoints -> select GET -> Send

## Morpheus

- Set `MORPHEUS_URL` and `MORPHEUS_TOKEN` in `apps/backend/.env`
- Visit `/morpheus` in UI to list Service Plans

## Auth Manager (M2)

- Choose environment and set header (e.g. `x-api-key`) in UI left panel
- Requests will include saved header for chosen env

## Codegen

- POST `/codegen/morpheus-plugin-stub.zip` to download plugin stub