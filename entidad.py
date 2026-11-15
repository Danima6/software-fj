"""
entidad.py
Clase abstracta base para todas las entidades del sistema
(clientes, servicios y reservas).
"""

from abc import ABC, abstractmethod  # ABC permite crear clases abstractas
import itertools                     # Para generar IDs consecutivos automáticamente


class Entidad(ABC):
    """Entidad general del sistema. No se puede instanciar directamente."""

    # Contador compartido por todas las entidades para asignar IDs únicos
    _contador_ids = itertools.count(1)

    def __init__(self):
        # Cada entidad recibe un ID único al crearse
        self._id = next(Entidad._contador_ids)

    @property
    def id(self):
        """Devuelve el ID (solo lectura, no se puede modificar desde afuera)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada clase hija DEBE implementar cómo se describe a sí misma."""
        pass

    @abstractmethod
    def validar(self):
        """Cada clase hija DEBE implementar sus propias validaciones."""
        pass

    def __str__(self):
        # Al imprimir cualquier entidad se usa su descripción
        return self.describir()
