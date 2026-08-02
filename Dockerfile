FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    FLASK_DEBUG=0 \
    FLASK_RUN_HOST=0.0.0.0 \
    ALLOW_EXTERNAL_DEBUG=0 \
    FLASK_RUN_PORT=5000

WORKDIR /app

# Install uv from the official image.
COPY --from=ghcr.io/astral-sh/uv:0.4.30@sha256:341e448d2ca38f11d8e2768db5464b4c95a4d87f539b8cb7511db86b02fef97e /uv /uvx /bin/

# Copy only dependency files first to maximize build cache.
COPY pyproject.toml uv.lock ./

# Create a project-local virtual environment and install locked deps.
RUN uv sync --frozen --no-dev

# Copy application source files.
COPY . .

EXPOSE 5000

CMD ["uv", "run", "python", "app.py"]
