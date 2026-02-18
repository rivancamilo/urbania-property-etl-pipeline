FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para MySQL y uv
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv - ahora se instala en /root/.local/bin/
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    mv /root/.local/bin/uvx /usr/local/bin/uvx && \
    uv --version

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias usando uv
RUN uv pip install --system -r requirements.txt

# Copiar código de la aplicación
COPY main.py .

# Crear directorio para datos XML
RUN mkdir -p /app/source

# Comando por defecto
CMD ["python", "main.py"]
