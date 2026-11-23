FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1

# Dependencies first for better layer caching
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

COPY main.py ./

ENV PATH="/app/.venv/bin:$PATH" \
    STATE_FILE=/data/state.json \
    OBSIDIAN_VAULT_PATH=/vault

VOLUME ["/data"]
CMD ["python", "main.py"]
