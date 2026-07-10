# Pinned by digest for reproducibility (python:3.12-slim, multi-arch manifest list).
FROM python:3.12-slim@sha256:423ed6ab25b1921a477529254bfeeabf5855151dc2c3141699a1bfc852199fbf

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

# Only the task input belongs in the agent image — no reference solution.
COPY access.log /app/access.log
