# Astra Architecture Overview

Astra is a mono-repo that provides an API Explorer & Integration Builder with a modern GUI and secure backend. It enables importing OpenAPI/Postman definitions, browsing endpoints, running requests, saving collections, generating typed SDKs, and scaffolding integrations. It includes a Morpheus connector with discover/diff/apply flows.

## Repo Layout

- apps/frontend: Next.js 14 + TypeScript UI, Tailwind + shadcn/ui, React Query, Zod, MSW
- apps/backend: FastAPI (Python 3.11), SQLModel + SQLite, Celery + Redis, httpx, OAuthlib
- packages/ui: shared UI components
- packages/sdk: SDK generation utilities (openapi-typescript + orval)
- packages/connectors: connector definitions and helpers (future TypeScript SDKs)

## Backend

- FastAPI app serves API endpoints: /openapi.json, /catalog, /requests, /connectors, /morpheus/*, /secrets
- SQLModel with SQLite (file) and easy swap to Postgres
- Celery worker + Redis for async tasks (discover/diff/apply), but synchronous stubs are provided for MVP
- Security: .env config, CORS hardened, security headers, Pydantic v2 validation, encrypted secrets at rest
- Errors use RFC 7807 (Problem Details) style

### Data model (MVP)
- ApiSpec (id, name, type, raw_json)
- SavedRequest (id, name, method, url, headers, params, body, spec_id?)
- AuditEvent (id, timestamp, actor, action, target, redacted_context)
- Secret (id, name, value_encrypted, created_at)

### Morpheus Connector (MVP)
- Auth: Bearer token
- Endpoints wrapped: /api/service-plans (Discover), placeholders for Diff/Apply with dry-run
- Idempotent helpers follow discover → diff → apply flow, dry-run returns a change plan

## Frontend

- App Router with pages for Workspace, Connectors, Codegen
- Request Builder: import OpenAPI (URL or file), browse tags/endpoints, build GET requests, run & view response, save as a Request
- Auth Manager: tokens and API keys (future)
- Connectors: Morpheus → Service Plans (Discover, Diff, Apply) with logs and export plan
- Codegen: Generate Morpheus Plugin Stub (Gradle project pinned to morpheus-plugin-api 1.2.8/1.2.9)

## Standards
- OpenAPI 3.1, JSON Schema
- JSON:API list/pagination
- AsyncAPI for webhooks (future)
- OAuth2/OIDC (Auth Code + PKCE)

## Packaging
- Dockerfiles for frontend and backend; docker-compose up exposes UI at http://localhost:3000 and API at http://localhost:8000

## CI/CD
- GitHub Actions: lint → unit → e2e → build → release (Docker images + Morpheus plugin stub zip)