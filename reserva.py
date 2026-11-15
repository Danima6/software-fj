"""
reserva.py
Clase Reserva: une un cliente, un servicio, una duración y un estado.
"""

from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)
from registro import registrar_evento, registrar_error


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    ESTADOS = ("pendiente", "confirmada", "cancelada", "procesada")

    def __init__(self, cliente, servicio, horas):
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        self.__estado = "pendiente"   # Toda reserva empieza pendiente
        self.__costo = None           # Se calcula al procesar
        self.validar()                # Primero valida...
        super().__init__()            # ...y solo si todo está bien recibe su ID

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def validar(self):
        if not isinstance(self.__cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido")
        if not isinstance(self.__servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido")
        if not isinstance(self.__horas, (int, float)) or self.__horas <= 0:
            raise ReservaInvalidaError(f"Duración inválida: {self.__horas} horas")
        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(f"'{self.__servicio.nombre}' no está disponible")

    def confirmar(self):
        """Pasa la reserva de 'pendiente' a 'confirmada'."""
        if self.__estado != "pendiente":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva #{self.id}: está '{self.__estado}'"
            )
        self.__estado = "confirmada"
        registrar_evento(f"Reserva #{self.id} confirmada")

    def cancelar(self):
        """Cancela la reserva (solo si no fue procesada ni cancelada antes)."""
        if self.__estado in ("cancelada", "procesada"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva #{self.id}: está '{self.__estado}'"
            )
        self.__estado = "cancelada"
        registrar_evento(f"Reserva #{self.id} cancelada")

    def procesar(self, con_iva=True, descuento=0.0):
        """
        Calcula el costo y marca la reserva como procesada.
        Usa try/except/else/finally y ENCADENAMIENTO de excepciones.
        """
        if self.__estado != "confirmada":
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas confirmadas (#{self.id} está '{self.__estado}')"
            )
        try:
            # Intentamos calcular el costo
            costo = self.__servicio.calcular_costo(self.__horas, con_iva, descuento)
        except CalculoInconsistenteError as e:
            # ENCADENAMIENTO: lanzamos un error de reserva que "envuelve" al original
            registrar_error(f"Fallo al procesar reserva #{self.id}: {e}")
            raise ReservaInvalidaError(f"No se pudo procesar la reserva #{self.id}") from e
        else:
            # Solo se ejecuta si NO hubo error
            self.__costo = costo
            self.__estado = "procesada"
            registrar_evento(f"Reserva #{self.id} procesada. Costo: ${costo:,.2f}")
        finally:
            # Se ejecuta SIEMPRE, haya error o no
            registrar_evento(f"Intento de procesamiento de reserva #{self.id} finalizado")
        return self.__costo

    def describir(self):
        return (f"Reserva #{self.id}: {self.__cliente.nombre} -> {self.__servicio.nombre} "
                f"({self.__horas} h) [{self.__estado}]")
