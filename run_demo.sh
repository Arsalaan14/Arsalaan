#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required for the one-command demo."
  echo "Install Docker Desktop, then run this script again."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose is required."
  exit 1
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

export APP_PORT="${APP_PORT:-8080}"
echo "Starting MediQueryNow demo..."
docker compose up --build -d

echo
echo "MediQueryNow is starting at: http://localhost:${APP_PORT}"
echo "Demo users are listed in DEMO_GUIDE.md"
echo
echo "To stop: docker compose down"
