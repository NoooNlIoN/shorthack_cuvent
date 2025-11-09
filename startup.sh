#!/usr/bin/env bash
set -euo pipefail

alembic upgrade head

python -m scripts.seed_data

exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"
