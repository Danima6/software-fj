"""
registro.py
Configura el archivo de logs donde se guardan eventos y errores.
Es el ÚNICO archivo que usa el sistema (no hay base de datos).
"""

import logging  # Módulo estándar de Python para registrar eventos

# Nombre del archivo donde se guardarán los logs
ARCHIVO_LOG = "software_fj.log"

# Configuración básica del logger:
logging.basicConfig(
    filename=ARCHIVO_LOG,                 # Archivo de destino
    level=logging.INFO,                   # Registra desde INFO hacia arriba (INFO, WARNING, ERROR)
    format="%(asctime)s | %(levelname)s | %(message)s",  # Formato: fecha | nivel | mensaje
    encoding="utf-8",                     # Para que se vean bien las tildes y la ñ
)

# Objeto logger que importarán los demás módulos
logger = logging.getLogger("SoftwareFJ")


def registrar_evento(mensaje):
    """Guarda un evento normal (algo que salió bien)."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Guarda un error en el archivo de logs."""
    logger.error(mensaje)
