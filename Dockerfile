# Etap budowania (builder)
FROM python:3.9-slim AS builder

LABEL org.opencontainers.image.authors="Piotr Zielinski"

ENV PYTHONUNBUFFERED=1

# Aktualizacja systemu, instalacja narzędzi build, aktualizacja pip i setuptools
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential curl && \
    pip install --upgrade pip==24.0 setuptools==78.1.1 && \
    pip install --no-cache-dir flask==3.0.3 requests==2.31.0 && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app.py /app

# Etap produkcyjny (runtime)
FROM python:3.9-slim

LABEL org.opencontainers.image.authors="Piotr Zielinski"

ENV PYTHONUNBUFFERED=1

# Aktualizacja systemu i pip w obrazie produkcyjnym
RUN apt-get update && \
    apt-get upgrade -y && \
    pip install --upgrade pip==24.0 setuptools==78.1.1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kopiowanie z buildera tylko niezbędnych bibliotek oraz kodu aplikacji
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000 || exit 1

CMD ["python", "app.py"]
