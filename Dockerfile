FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/
WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["fastapi", "run", "src/subnet_calculator_sqa/api.py", "--host", "0.0.0.0", "--port", "8000"]