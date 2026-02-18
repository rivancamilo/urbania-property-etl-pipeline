import xml.etree.ElementTree as et
import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import Dict, List, Any
import logging
import os


class XMLToMySQLProcessor:
    """
    Clase para procesar archivos XML y cargarlos en MySQL.
    """
    def __init__(self, xml_file: str, db_config: Dict[str, str]):
        """
        Inicializa el procesador
        """
        self.xml_file = xml_file
        self.db_config = db_config
        self.connection = None
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """Configura el logger."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    
    def extraccion_xml(self):
        """Extrae datos del archivo XML."""
        try:
            self.logger.info(f"Parseando archivo XML: {self.xml_file}")
            
            idPropiedad = 9999
            usuarios = []
            propiedades = []
            
            arbol = et.parse(self.xml_file) 
            data2 = arbol.findall('listing')
            
            for indice, registro in enumerate(data2, start=1):
                estado = registro.find('state').text
                ciudad = registro.find('city').text
                colonia = registro.find('colony').text
                calle = registro.find('street').text
                numero_exterior = registro.find('external_num').text
                tipo_inmueble = registro.find('type').text
                transaccion = registro.find('purpose').text
                precio = registro.find('price').text
                codigo_proveedor = registro.find('code').text
                correo_contacto = registro.find('mail_contact').text
                telefono_contacto = registro.find('phone_contact').text
                
                usuarios.append({
                    'idusuario': indice, 
                    'correo_contacto': correo_contacto
                })
                
                propiedades.append({
                    'idpropiedad': idPropiedad + indice,
                    'estado': estado,
                    'ciudad': ciudad,
                    'colonia': colonia,
                    'calle': calle,
                    'numero_exterior': numero_exterior,
                    'tipo_inmueble': tipo_inmueble,
                    'transaccion': transaccion,
                    'precio': precio,
                    'codigo_proveedor': codigo_proveedor,
                    'telefono_contacto': telefono_contacto,
                    'idusuario': indice
                })
            
            self.logger.info(f"Extraídos {len(usuarios)} usuarios y {len(propiedades)} propiedades")
            return usuarios, propiedades
            
        except et.ParseError as e:
            self.logger.error(f"Error al parsear XML: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")
            raise
        
    def connect_db(self):
        """Establece conexión con MySQL."""
        try:
            self.logger.info(f"Conectando a MySQL en {self.db_config['host']}:{self.db_config['port']}")
            
            self.connection = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database'],
                port=self.db_config.get('port', 3306)
            )
            
            if self.connection.is_connected():
                self.logger.info("Conexión a MySQL exitosa")
                
        except Error as e:
            self.logger.error(f"Error conectando a MySQL: {e}")
            raise    
        
    def cargar_usuario(self, datos):
        """Inserta usuarios en la tabla usuarios."""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO usuarios (correo_contacto)
                VALUES (%s)
            """
            
            datos_usuarios = [usuario['correo_contacto'] for usuario in datos]
            datos_tuplas = [(correo,) for correo in datos_usuarios]
            
            cursor.executemany(query, datos_tuplas)
            self.connection.commit()
            
            self.logger.info(f"{len(datos)} registros insertados en la tabla de Usuarios")
            cursor.close()
            
        except Error as e:
            self.logger.error(f"Error insertando usuarios: {e}")
            raise
       
    def cargar_propiedades(self, datos):
        """Inserta propiedades en la tabla propiedades."""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO propiedades (
                    idpropiedad, estado, ciudad, colonia, calle, 
                    numero_exterior, tipo_inmueble, transaccion, precio, 
                    codigo_proveedor, telefono_contacto, idusuario
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            datos_tuplas = [
                (
                    prop['idpropiedad'],
                    prop['estado'],
                    prop['ciudad'],
                    prop['colonia'],
                    prop['calle'],
                    prop['numero_exterior'],
                    prop['tipo_inmueble'],
                    prop['transaccion'],
                    prop['precio'],
                    prop['codigo_proveedor'],
                    prop['telefono_contacto'],
                    prop['idusuario']
                )
                for prop in datos
            ]
            
            cursor.executemany(query, datos_tuplas)
            self.connection.commit()
            
            self.logger.info(f"{len(datos)} registros insertados en la tabla de Propiedades")
            cursor.close()
            
        except Error as e:
            self.logger.error(f"Error insertando propiedades: {e}")
            raise
       
    def close_connection(self):
        """Cierra la conexión a MySQL."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Conexión a MySQL cerrada")
    
    def process(self):
        """Ejecuta el proceso completo: parsear XML y cargar a MySQL."""
        try:
            # 1. Parsear XML
            usuarios, propiedades = self.extraccion_xml()
            
            # 2. Conectar a BD
            self.connect_db()
            
            # 3. Cargar datos
            self.cargar_usuario(usuarios)
            self.cargar_propiedades(propiedades)
            
            self.logger.info("✓ Proceso completado exitosamente")
            
        except Exception as e:
            self.logger.error(f"Error en el proceso: {e}")
            raise
        finally:
            self.close_connection()


def get_db_config():
    """Obtiene configuración de BD desde variables de entorno o valores por defecto."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'rootpassword'),
        'database': os.getenv('DB_NAME', 'bdUrbania'),
        'port': int(os.getenv('DB_PORT', '3306'))
    }


def get_xml_file():
    """Obtiene ruta del archivo XML desde variables de entorno."""
    return os.getenv('XML_FILE', './source/feed.xml')


if __name__ == "__main__":
    # Configuración desde variables de entorno
    db_config = get_db_config()
    xml_file = get_xml_file()
    
    # Log de configuración
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    logger.info(f"Configuración: DB={db_config['host']}:{db_config['port']}, XML={xml_file}")
    
    # Ejecutar proceso
    processor = XMLToMySQLProcessor(xml_file, db_config)
    processor.process()