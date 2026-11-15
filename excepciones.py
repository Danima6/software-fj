"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.

Todas heredan de una excepción base (SoftwareFJError) para poder
capturar cualquier error propio del sistema con un solo 'except'.
"""


# Excepción base: todas las demás heredan de esta
class SoftwareFJError(Exception):
    """Error general del sistema Software FJ."""
    pass  # No necesita lógica extra; sirve como "familia" de errores


# --- Errores relacionados con clientes ---
class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no son válidos."""
    pass


# --- Errores relacionados con servicios ---
class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando un servicio se crea con parámetros incorrectos."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""
    pass


# --- Errores relacionados con reservas ---
class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva tiene datos incorrectos (ej. duración negativa)."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una acción no válida (ej. cancelar algo ya cancelado)."""
    pass


# --- Errores de cálculo ---
class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costo da un resultado imposible (ej. negativo)."""
    pass
