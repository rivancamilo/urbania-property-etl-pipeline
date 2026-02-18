-- Script para configurar permisos de Airflow
-- Este script se ejecutará después de BDUrbania.sql

-- NOTA: El usuario 'airflow_user' y la base de datos 'airflow_db' 
-- ya fueron creados automáticamente por las variables de entorno del Dockerfile:
--   MYSQL_DATABASE=airflow_db
--   MYSQL_USER=airflow_user
--   MYSQL_PASSWORD=airflow_password

-- Solo necesitamos dar permisos adicionales en bdUrbania para ETL
GRANT SELECT, INSERT, UPDATE, DELETE ON bdUrbania.* TO 'airflow_user'@'%';

-- También dar permisos al root para acceder a bdUrbania
GRANT ALL PRIVILEGES ON bdUrbania.* TO 'root'@'%';

FLUSH PRIVILEGES;