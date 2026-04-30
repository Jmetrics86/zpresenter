# syntax=docker/dockerfile:1

FROM node:22-bookworm-slim AS web-build
WORKDIR /w
COPY webapp/package.json webapp/package-lock.json ./
RUN npm ci
COPY webapp/ ./
RUN npm run build

FROM python:3.12-slim-bookworm
WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
COPY src ./src
COPY examples ./examples
COPY schemas ./schemas
COPY --from=web-build /w/dist ./webapp/dist

RUN uv sync --frozen --no-dev \
    --extra ai-anthropic \
    --extra ai-openai \
    --extra ai-gemini

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "zpresenter.server:app", "--host", "0.0.0.0", "--port", "8000"]
