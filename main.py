"""
main.py
Programa principal: simula más de 10 operaciones (válidas e inválidas)
y demuestra que el sistema sigue funcionando aunque ocurran errores.

Ejecutar con:  python main.py
"""

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import SoftwareFJError
from registro import registrar_evento, registrar_error, ARCHIVO_LOG

# "Base de datos" en memoria: solo listas de objetos
clientes = []
servicios = []
reservas = []


def ejecutar(numero, descripcion, funcion):
    """
    Ejecuta una operación protegida con try/except.
    Si falla, registra el error y el programa CONTINÚA con la siguiente.
    """
    print(f"\nOperación {numero}: {descripcion}")
    try:
        resultado = funcion()
    except SoftwareFJError as e:
        # Errores propios del sistema (los esperados)
        print(f"   ✗ Error controlado: {e}")
        if e.__cause__:  # Si hubo encadenamiento, mostramos la causa original
            print(f"     Causa original: {e.__cause__}")
        registrar_error(f"Op {numero} ({descripcion}): {e}")
    except Exception as e:
        # Cualquier otro error inesperado: tampoco detiene el programa
        print(f"   ✗ Error inesperado: {type(e).__name__}: {e}")
        registrar_error(f"Op {numero} inesperado: {type(e).__name__}: {e}")
    else:
        print(f"   ✓ OK: {resultado}")
        registrar_evento(f"Op {numero} ({descripcion}) exitosa")


# ---------- Funciones auxiliares para cada operación ----------
def crear_cliente(*datos):
    c = Cliente(*datos)
    clientes.append(c)
    return c


def crear_servicio(clase, *datos):
    s = clase(*datos)
    servicios.append(s)
    return s


def crear_reserva(cliente, servicio, horas):
    r = Reserva(cliente, servicio, horas)
    reservas.append(r)
    return r


def confirmar_y_procesar(reserva, descuento=0.0):
    reserva.confirmar()
    costo = reserva.procesar(con_iva=True, descuento=descuento)
    return f"{reserva} | Total con IVA: ${costo:,.2f}"


def main():
    registrar_evento("===== Inicio de la simulación =====")
    print("=== SISTEMA SOFTWARE FJ ===")

    # --- Clientes ---
    ejecutar(1, "Registrar cliente válido",
             lambda: crear_cliente("Ana Gomez", "1012345678", "ana@correo.com", "3001234567"))
    ejecutar(2, "Registrar cliente con correo inválido",
             lambda: crear_cliente("Pedro Ruiz", "1098765432", "pedro-correo", "3109876543"))
    ejecutar(3, "Registrar cliente con documento con letras",
             lambda: crear_cliente("Laura Diaz", "ABC123", "laura@correo.com", "3201112233"))
    ejecutar(4, "Registrar segundo cliente válido",
             lambda: crear_cliente("Carlos Perez", "79123456", "carlos@empresa.co", "3157778899"))

    # --- Servicios ---
    ejecutar(5, "Crear sala de reuniones válida",
             lambda: crear_servicio(ReservaSala, "Sala Andes", 50000, 25))
    ejecutar(6, "Crear sala con capacidad imposible (0)",
             lambda: crear_servicio(ReservaSala, "Sala Fantasma", 40000, 0))
    ejecutar(7, "Crear alquiler de equipos válido",
             lambda: crear_servicio(AlquilerEquipo, "Portátil", 15000, 3))
    ejecutar(8, "Crear asesoría con nivel inexistente",
             lambda: crear_servicio(Asesoria, "Asesoría Python", 80000, "master"))
    ejecutar(9, "Crear asesoría válida",
             lambda: crear_servicio(Asesoria, "Asesoría Python", 80000, "experto"))
    ejecutar(10, "Crear servicio con tarifa negativa",
             lambda: crear_servicio(AlquilerEquipo, "Proyector", -5000, 1))

    ana, carlos = clientes[0], clientes[1]
    sala, portatiles, asesoria = servicios[0], servicios[1], servicios[2]

    # --- Reservas ---
    r1 = None

    def reserva_exitosa():
        nonlocal r1
        r1 = crear_reserva(ana, sala, 3)
        return confirmar_y_procesar(r1)

    ejecutar(11, "Reserva exitosa de sala (3 h)", reserva_exitosa)
    ejecutar(12, "Reserva con duración negativa",
             lambda: crear_reserva(carlos, portatiles, -2))

    def reservar_no_disponible():
        asesoria.cambiar_disponibilidad(False)  # El experto no está disponible
        return crear_reserva(carlos, asesoria, 2)

    ejecutar(13, "Reservar asesoría no disponible", reservar_no_disponible)
    ejecutar(14, "Cancelar una reserva ya procesada", lambda: r1.cancelar())

    def descuento_invalido():
        r = crear_reserva(carlos, portatiles, 4)
        return confirmar_y_procesar(r, descuento=1.5)  # 150 % de descuento: imposible

    ejecutar(15, "Procesar con descuento imposible (encadenamiento)", descuento_invalido)

    def reserva_con_descuento():
        r = crear_reserva(carlos, portatiles, 4)
        return confirmar_y_procesar(r, descuento=0.10)

    ejecutar(16, "Reserva exitosa con 10 % de descuento", reserva_con_descuento)
    ejecutar(17, "Reserva sin cliente (dato faltante)",
             lambda: crear_reserva(None, sala, 1))

    # --- Resumen final ---
    print("\n=== RESUMEN ===")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios creados:    {len(servicios)}")
    print(f"Reservas creadas:     {len(reservas)}")
    for r in reservas:
        print("  -", r)
    print(f"\nEl sistema terminó sin detenerse. Revise el archivo '{ARCHIVO_LOG}'.")
    registrar_evento("===== Fin de la simulación =====")


# Solo se ejecuta si se corre este archivo directamente
if __name__ == "__main__":
    main()
