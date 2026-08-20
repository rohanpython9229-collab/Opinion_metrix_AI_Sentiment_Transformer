#!/bin/sh

echo "=== OpinionAI START.SH STARTED ==="

uvicorn api.main:app --host 0.0.0.0 --port 8000 &

API_PID=$!

echo "=== FastAPI PID: $API_PID ==="

sleep 5

echo "=== Starting Streamlit ==="

exec streamlit run app.py \
  --server.address=0.0.0.0 \
  --server.port=${PORT:-8501} \
  --server.fileWatcherType=none