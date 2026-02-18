CREATE DATABASE IF NOT EXISTS bdUrbania CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE bdUrbania;

CREATE TABLE IF NOT EXISTS usuarios (
  idusuario int NOT NULL AUTO_INCREMENT,
  correo_contacto varchar(150) NOT NULL,
  PRIMARY KEY (idusuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS propiedades (
  idpropiedad int NOT NULL AUTO_INCREMENT,
  estado varchar(100) NOT NULL,
  ciudad varchar(50) NOT NULL,
  colonia varchar(250) NOT NULL,
  calle varchar(250) DEFAULT NULL,
  numero_exterior varchar(50) DEFAULT NULL,
  tipo_inmueble varchar(70) NOT NULL,
  transaccion varchar(70) NOT NULL,
  precio decimal(38,0) NOT NULL,
  codigo_proveedor int NOT NULL,
  telefono_contacto varchar(45) NOT NULL,
  idusuario int NOT NULL,
  PRIMARY KEY (idpropiedad),
  KEY idusuario (idusuario),
  CONSTRAINT propiedades_ibfk_1 FOREIGN KEY (idusuario) REFERENCES usuarios (idusuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

COMMIT;