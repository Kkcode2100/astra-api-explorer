# syntax=docker/dockerfile:1
FROM node:20-alpine AS base
WORKDIR /app

COPY package.json pnpm-lock.yaml* ./
RUN corepack enable && corepack prepare pnpm@9.7.0 --activate && pnpm install --frozen-lockfile || true

COPY . .
RUN pnpm build || true
EXPOSE 3000
CMD ["pnpm", "start"]