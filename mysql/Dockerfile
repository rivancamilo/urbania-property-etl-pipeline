# mysql/Dockerfile
FROM mysql:8.0

# Copiar scripts de inicialización
# MySQL ejecutará todos los scripts .sql en /docker-entrypoint-initdb.d/ en orden alfabético
COPY BDUrbania.sql /docker-entrypoint-initdb.d/01-BDUrbania.sql

# Crear script para base de datos de Airflow
COPY init-airflow-db.sql /docker-entrypoint-initdb.d/02-init-airflow-db.sql

# Configuración de MySQL
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=airflow_db
ENV MYSQL_USER=airflow_user
ENV MYSQL_PASSWORD=airflow_password

# Exponer puerto
EXPOSE 3306
