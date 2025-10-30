# ---------------- Builder Stage ----------------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------------- Runtime Stage ----------------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY . .

EXPOSE 5001

ENTRYPOINT ["python", "serving/serve.py"]
