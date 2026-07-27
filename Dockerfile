FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv from the official image.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy only dependency files first to maximize build cache.
COPY pyproject.toml uv.lock ./

# Create a project-local virtual environment and install locked deps.
RUN uv sync --frozen --no-dev

# Copy application source files.
COPY . .

EXPOSE 5000

CMD ["uv", "run", "python", "app.py"]
