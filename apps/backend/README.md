## Astra Backend

FastAPI + SQLModel backend for Astra.

- Run locally: `uvicorn main:app --reload`
- Env: copy `.env.example` to `.env`
- Endpoints:
  - `/health`
  - `/openapi.json`
  - `/specs` (import, list, endpoints)
  - `/requests/send` (send arbitrary HTTP request)
  - `/morpheus/service-plans/*` (discover, diff, apply)
  - `/codegen/morpheus-plugin-stub.zip` (zip generator)