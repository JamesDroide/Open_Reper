FROM python:3.10-slim as builder

ENV REFLEX_ENV=production \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH="/app:${PYTHONPATH}"

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt tensorflow-cpu==2.12.0

FROM python:3.10-slim

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app
COPY . .

RUN chmod -R a+r /app/models && \
    mv /app/models/* /app/models/  # Asegurar ubicación

RUN python -c "from open_reper.open_reper import app; app.compile()"

EXPOSE 3000 8001

CMD ["python", "-m", "open_reper.open_reper", "--backend-port", "8001", "--host", "0.0.0.0"]