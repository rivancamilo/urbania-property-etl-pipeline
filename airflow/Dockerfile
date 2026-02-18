FROM apache/airflow:2.8.1-python3.11

USER root

# Instalar dependencias del sistema necesarias para MySQL y netcat para health checks
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar script de inicio
COPY start-airflow.sh /start-airflow.sh
RUN chmod +x /start-airflow.sh

USER airflow

# Copiar requirements.txt
COPY requirements.txt /requirements.txt

# Instalar paquetes Python necesarios para MySQL y Airflow
# IMPORTANTE: Instalamos en el orden correcto para evitar conflictos
RUN pip install --no-cache-dir \
    apache-airflow-providers-mysql==5.5.2 \
    mysql-connector-python==8.2.0 \
    pymysql==1.1.0

# Instalar dependencias adicionales del requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Establecer el directorio de trabajo
WORKDIR /opt/airflow

# El script de inicio se ejecutará desde docker-compose