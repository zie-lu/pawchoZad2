FROM python:3.9-slim AS builder

LABEL org.opencontainers.image.authors="Piotr Zielinski"

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    pip install --upgrade pip && \
    pip install --no-cache-dir flask requests && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app.py /app

FROM python:3.9-slim

LABEL org.opencontainers.image.authors="Piotr Zielinski"

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000 || exit 1

CMD ["python", "app.py"]