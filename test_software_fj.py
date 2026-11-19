"""
test_software_fj.py
Pruebas unitarias con unittest para el sistema Software FJ.
Valida el funcionamiento correcto y el lanzamiento de excepciones en:
- Cliente
- Servicios (ReservaSala, AlquilerEquipo, Asesoria)
- Reserva (flujo de estados, cálculos y encadenamiento de excepciones)

Ejecutar con: python -m unittest test_software_fj.py -v
"""

import unittest

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)


class TestCliente(unittest.TestCase):
    """Pruebas unitarias para la clase Cliente."""

    def test_crear_cliente_valido(self):
        cliente = Cliente("Ana Gomez", "1012345678", "ana@correo.com", "3001234567")
        self.assertEqual(cliente.nombre, "Ana Gomez")
        self.assertEqual(cliente.documento, "1012345678")
        self.assertEqual(cliente.correo, "ana@correo.com")
        self.assertEqual(cliente.telefono, "3001234567")
        self.assertIsInstance(cliente.id, int)

    def test_actualizar_telefono_valido(self):
        cliente = Cliente("Carlos Perez", "79123456", "carlos@empresa.co", "3157778899")
        cliente.telefono = "3209998877"
        self.assertEqual(cliente.telefono, "3209998877")

    def test_nombre_invalido_lanza_excepcion(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("", "1012345678", "ana@correo.com", "3001234567")
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana123", "1012345678", "ana@correo.com", "3001234567")

    def test_documento_invalido_lanza_excepcion(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Laura Diaz", "ABC123", "laura@correo.com", "3201112233")
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Laura Diaz", "123", "laura@correo.com", "3201112233")

    def test_correo_invalido_lanza_excepcion(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Pedro Ruiz", "1098765432", "pedro-correo", "3109876543")

    def test_telefono_invalido_lanza_excepcion(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana Gomez", "1012345678", "ana@correo.com", "12345")

        cliente = Cliente("Ana Gomez", "1012345678", "ana@correo.com", "3001234567")
        with self.assertRaises(ClienteInvalidoError):
            cliente.telefono = "no_numerico"


class TestServicios(unittest.TestCase):
    """Pruebas unitarias para ReservaSala, AlquilerEquipo y Asesoria."""

    def test_reserva_sala_calculo_y_recargo(self):
        # Sala pequeña (<= 20 personas): sin recargo
        sala_pequena = ReservaSala("Sala Norte", 50000, 10)
        self.assertEqual(sala_pequena.costo_base(2), 100000.0)

        # Sala grande (> 20 personas): 20% de recargo
        sala_grande = ReservaSala("Sala Andes", 50000, 25)
        self.assertEqual(sala_grande.costo_base(2), 120000.0)
        # Con IVA (19%) y 10% descuento: 120000 * 0.9 * 1.19 = 128520.0
        self.assertEqual(sala_grande.calcular_costo(2, con_iva=True, descuento=0.10), 128520.0)

    def test_alquiler_equipo_calculo(self):
        equipos = AlquilerEquipo("Portátil", 15000, 3)
        self.assertEqual(equipos.costo_base(4), 180000.0)
        self.assertEqual(equipos.calcular_costo(4, con_iva=True), 214200.0)

    def test_asesoria_calculo_por_nivel(self):
        asesoria_basica = Asesoria("Soporte", 80000, "basico")
        asesoria_experta = Asesoria("Arquitectura", 80000, "experto")
        self.assertEqual(asesoria_basica.costo_base(2), 160000.0)
        self.assertEqual(asesoria_experta.costo_base(2), 320000.0)

    def test_servicios_parametros_invalidos(self):
        # Tarifa negativa o cero
        with self.assertRaises(ServicioInvalidoError):
            AlquilerEquipo("Proyector", -5000, 1)
        # Nombre vacío
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("", 40000, 10)
        # Capacidad de sala fuera de rango (1..50)
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("Sala Fantasma", 40000, 0)
        with self.assertRaises(ServicioInvalidoError):
            ReservaSala("Estadio", 40000, 60)
        # Cantidad de equipos inválida
        with self.assertRaises(ServicioInvalidoError):
            AlquilerEquipo("Mouse", 5000, 0)
        # Nivel de asesoría inexistente
        with self.assertRaises(ServicioInvalidoError):
            Asesoria("Asesoría Python", 80000, "master")

    def test_descuento_fuera_de_rango_lanza_excepcion(self):
        sala = ReservaSala("Sala Sur", 50000, 10)
        with self.assertRaises(CalculoInconsistenteError):
            sala.calcular_costo(2, descuento=1.5)
        with self.assertRaises(CalculoInconsistenteError):
            sala.calcular_costo(2, descuento=-0.1)


class TestReserva(unittest.TestCase):
    """Pruebas unitarias para el ciclo de vida y validaciones de Reserva."""

    def setUp(self):
        """Se ejecuta antes de cada prueba para preparar objetos limpios."""
        self.cliente = Cliente("Luis Duenas", "1098765432", "luis@unad.edu.co", "3005554433")
        self.servicio = ReservaSala("Sala Ejecutiva", 50000, 15)

    def test_flujo_completo_reserva_exitosa(self):
        reserva = Reserva(self.cliente, self.servicio, 3)
        self.assertEqual(reserva.estado, "pendiente")
        self.assertIsNone(reserva.costo)

        reserva.confirmar()
        self.assertEqual(reserva.estado, "confirmada")

        costo_final = reserva.procesar(con_iva=True, descuento=0.10)
        # 50000 * 3 = 150000 -> -10% = 135000 -> +19% IVA = 160650.0
        self.assertEqual(costo_final, 160650.0)
        self.assertEqual(reserva.costo, 160650.0)
        self.assertEqual(reserva.estado, "procesada")

    def test_cancelar_reserva_pendiente(self):
        reserva = Reserva(self.cliente, self.servicio, 2)
        reserva.cancelar()
        self.assertEqual(reserva.estado, "cancelada")

    def test_validaciones_creacion_reserva(self):
        # Cliente inválido
        with self.assertRaises(ReservaInvalidaError):
            Reserva(None, self.servicio, 2)
        # Servicio inválido
        with self.assertRaises(ReservaInvalidaError):
            Reserva(self.cliente, "no_es_servicio", 2)
        # Horas negativas o cero
        with self.assertRaises(ReservaInvalidaError):
            Reserva(self.cliente, self.servicio, -2)
        with self.assertRaises(ReservaInvalidaError):
            Reserva(self.cliente, self.servicio, 0)

    def test_reservar_servicio_no_disponible(self):
        self.servicio.cambiar_disponibilidad(False)
        with self.assertRaises(ServicioNoDisponibleError):
            Reserva(self.cliente, self.servicio, 2)

    def test_operaciones_no_permitidas_por_estado(self):
        reserva = Reserva(self.cliente, self.servicio, 2)

        # No se puede procesar sin confirmar antes
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.procesar()

        reserva.confirmar()
        # No se puede confirmar dos veces
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.confirmar()

        reserva.procesar()
        # No se puede cancelar una reserva ya procesada
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()

    def test_encadenamiento_excepcion_al_procesar(self):
        reserva = Reserva(self.cliente, self.servicio, 2)
        reserva.confirmar()

        with self.assertRaises(ReservaInvalidaError) as contexto:
            reserva.procesar(con_iva=True, descuento=1.5)

        # Verifica que la causa original sea CalculoInconsistenteError (raise ... from e)
        self.assertIsInstance(contexto.exception.__cause__, CalculoInconsistenteError)


if __name__ == "__main__":
    unittest.main()