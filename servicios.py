"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
- ReservaSala
- AlquilerEquipo
- Asesoria

Cada uno sobrescribe calcular_costo(), describir() y validar_parametros()
(eso es POLIMORFISMO: mismo método, comportamiento distinto).
"""

from abc import abstractmethod

from entidad import Entidad
from excepciones import ServicioInvalidoError, CalculoInconsistenteError

IVA = 0.19  # Impuesto por defecto en Colombia (19 %)


class Servicio(Entidad):
    """Servicio general. No se puede instanciar directamente."""

    def __init__(self, nombre, tarifa_hora, disponible=True):
        self._nombre = nombre
        self._tarifa_hora = tarifa_hora
        self._disponible = disponible
        self.validar()          # Primero valida...
        super().__init__()      # ...y solo si todo está bien recibe su ID

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        """Activa o desactiva el servicio."""
        self._disponible = bool(estado)

    def validar(self):
        """Validaciones comunes a todos los servicios."""
        if not self._nombre:
            raise ServicioInvalidoError("El servicio debe tener un nombre")
        if not isinstance(self._tarifa_hora, (int, float)) or self._tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida para '{self._nombre}': {self._tarifa_hora}")
        self.validar_parametros()  # Validaciones propias de cada servicio hijo

    # ----- Métodos que cada hijo DEBE implementar -----
    @abstractmethod
    def validar_parametros(self):
        pass

    @abstractmethod
    def costo_base(self, horas):
        """Costo sin impuestos ni descuentos."""
        pass

    # ----- Método "sobrecargado" -----
    # Python no permite varios métodos con el mismo nombre, así que la
    # sobrecarga se simula con parámetros opcionales. Se puede llamar:
    #   calcular_costo(horas)                       -> solo costo base
    #   calcular_costo(horas, con_iva=True)         -> con impuesto
    #   calcular_costo(horas, descuento=0.1)        -> con descuento
    #   calcular_costo(horas, True, 0.1)            -> con ambos
    def calcular_costo(self, horas, con_iva=False, descuento=0.0):
        if not 0 <= descuento < 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango: {descuento}")
        total = self.costo_base(horas)          # Polimorfismo: cada hijo calcula distinto
        total = total * (1 - descuento)         # Aplica el descuento
        if con_iva:
            total = total * (1 + IVA)           # Aplica el IVA
        if total < 0:
            raise CalculoInconsistenteError(f"El costo no puede ser negativo: {total}")
        return round(total, 2)


class ReservaSala(Servicio):
    """Reserva de salas de reuniones."""

    def __init__(self, nombre, tarifa_hora, capacidad):
        self._capacidad = capacidad  # Se asigna ANTES de super() porque validar() lo usa
        super().__init__(nombre, tarifa_hora)

    def validar_parametros(self):
        if not isinstance(self._capacidad, int) or not 1 <= self._capacidad <= 50:
            raise ServicioInvalidoError(f"Capacidad de sala inválida: {self._capacidad}")

    def costo_base(self, horas):
        # Salas grandes (más de 20 personas) cuestan 20 % más
        recargo = 1.2 if self._capacidad > 20 else 1.0
        return self._tarifa_hora * horas * recargo

    def describir(self):
        return f"Sala '{self._nombre}' para {self._capacidad} personas (${self._tarifa_hora}/h)"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portátiles, proyectores, etc.)."""

    def __init__(self, nombre, tarifa_hora, cantidad):
        self._cantidad = cantidad
        super().__init__(nombre, tarifa_hora)

    def validar_parametros(self):
        if not isinstance(self._cantidad, int) or self._cantidad <= 0:
            raise ServicioInvalidoError(f"Cantidad de equipos inválida: {self._cantidad}")

    def costo_base(self, horas):
        # Se cobra por equipo y por hora
        return self._tarifa_hora * horas * self._cantidad

    def describir(self):
        return f"Alquiler de {self._cantidad} x '{self._nombre}' (${self._tarifa_hora}/h c/u)"


class Asesoria(Servicio):
    """Asesoría especializada con un experto."""

    NIVELES = {"basico": 1.0, "intermedio": 1.5, "experto": 2.0}  # Multiplicador por nivel

    def __init__(self, nombre, tarifa_hora, nivel):
        self._nivel = nivel
        super().__init__(nombre, tarifa_hora)

    def validar_parametros(self):
        if self._nivel not in Asesoria.NIVELES:
            raise ServicioInvalidoError(f"Nivel de asesoría inválido: '{self._nivel}'")

    def costo_base(self, horas):
        return self._tarifa_hora * horas * Asesoria.NIVELES[self._nivel]

    def describir(self):
        return f"Asesoría '{self._nombre}' nivel {self._nivel} (${self._tarifa_hora}/h)"
