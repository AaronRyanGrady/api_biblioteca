# ---------- Etapa 1: builder ----------
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# Herramientas de compilación (para posibles wheels; psycopg2-binary ya trae libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Entorno virtual para aislar dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instala dependencias (tus versiones de la prueba técnica)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Etapa 2: runtime ----------
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/opt/venv/bin:$PATH"
WORKDIR /app

# Utilidades mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl tini && \
    rm -rf /var/lib/apt/lists/*

# Copia el venv resuelto y el código
COPY --from=builder /opt/venv /opt/venv
COPY . /app

# Usuario no root
RUN useradd -ms /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

# Puerto de la API
EXPOSE 8000

# Healthcheck (requiere endpoint /health)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1

# Arranque en producción
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["gunicorn","app.main:app","-k","uvicorn.workers.UvicornWorker","-b","0.0.0.0:8000","--workers","1","--timeout","60","--access-logfile","-","--error-logfile","-"]
