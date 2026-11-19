"""
main.py
Programa principal de Software FJ: incluye menÃº interactivo por consola
para registrar clientes, crear servicios y gestionar reservas con manejo
de excepciones, ademÃ¡s de una opciÃ³n para ejecutar la simulaciÃ³n de pruebas.

Ejecutar con:  python main.py
"""

from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reserva import Reserva
from excepciones import SoftwareFJError
from registro import registrar_evento, registrar_error, ARCHIVO_LOG

# "Base de datos" en memoria
clientes = []
servicios = []
reservas = []


# ---------- Funciones auxiliares de negocio ----------
def crear_cliente(nombre, documento, correo, telefono):
    c = Cliente(nombre, documento, correo, telefono)
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


# ---------- Opciones del menÃº interactivo ----------
def opcion_registrar_cliente():
    print("\n--- REGISTRAR NUEVO CLIENTE ---")
    nombre = input("Nombre completo (solo letras): ").strip()
    documento = input("Documento (6 a 10 dÃ­gitos): ").strip()
    correo = input("Correo electrÃ³nico: ").strip()
    telefono = input("TelÃ©fono (10 dÃ­gitos): ").strip()

    cliente = crear_cliente(nombre, documento, correo, telefono)
    print(f"âœ“ Cliente registrado con Ã©xito: {cliente}")
    registrar_evento(f"MenÃº: Cliente registrado ({cliente})")


def opcion_crear_servicio():
    print("\n--- CREAR NUEVO SERVICIO ---")
    print("Seleccione el tipo de servicio:")
    print("  1. Reserva de Sala")
    print("  2. Alquiler de Equipo")
    print("  3. AsesorÃ­a Especializada")
    tipo = input("OpciÃ³n (1-3): ").strip()

    if tipo not in ("1", "2", "3"):
        raise ValueError("Tipo de servicio invÃ¡lido. Debe elegir 1, 2 o 3.")

    nombre = input("Nombre del servicio: ").strip()
    try:
        tarifa = float(input("Tarifa por hora ($): ").strip())
    except ValueError:
        raise ValueError("La tarifa por hora debe ser un valor numÃ©rico vÃ¡lido.")

    if tipo == "1":
        try:
            capacidad = int(input("Capacidad de personas (1 a 50): ").strip())
        except ValueError:
            raise ValueError("La capacidad debe ser un nÃºmero entero.")
        servicio = crear_servicio(ReservaSala, nombre, tarifa, capacidad)

    elif tipo == "2":
        try:
            cantidad = int(input("Cantidad de equipos disponibles: ").strip())
        except ValueError:
            raise ValueError("La cantidad de equipos debe ser un nÃºmero entero.")
        servicio = crear_servicio(AlquilerEquipo, nombre, tarifa, cantidad)

    elif tipo == "3":
        nivel = input("Nivel (basico / intermedio / experto): ").strip().lower()
        servicio = crear_servicio(Asesoria, nombre, tarifa, nivel)

    print(f"âœ“ Servicio creado con Ã©xito: {servicio}")
    registrar_evento(f"MenÃº: Servicio creado ({servicio})")


def opcion_hacer_reserva():
    print("\n--- CREAR Y GESTIONAR RESERVA ---")
    if not clientes:
        print("âš  No hay clientes registrados. Registre un cliente primero.")
        return
    if not servicios:
        print("âš  No hay servicios creados. Cree un servicio primero.")
        return

    print("\nClientes disponibles:")
    for c in clientes:
        print(f"  ID {c.id} -> {c.describir()}")

    try:
        id_cliente = int(input("Ingrese el ID del cliente: ").strip())
    except ValueError:
        raise ValueError("El ID del cliente debe ser un nÃºmero entero.")

    cliente_sel = next((c for c in clientes if c.id == id_cliente), None)
    if not cliente_sel:
        raise ValueError(f"No existe ningÃºn cliente con ID {id_cliente}.")

    print("\nServicios disponibles:")
    for s in servicios:
        estado_disp = "Disponible" if s.disponible else "No disponible"
        print(f"  ID {s.id} -> {s.describir()} [{estado_disp}]")

    try:
        id_servicio = int(input("Ingrese el ID del servicio: ").strip())
    except ValueError:
        raise ValueError("El ID del servicio debe ser un nÃºmero entero.")

    servicio_sel = next((s for s in servicios if s.id == id_servicio), None)
    if not servicio_sel:
        raise ValueError(f"No existe ningÃºn servicio con ID {id_servicio}.")

    try:
        horas = float(input("DuraciÃ³n de la reserva (horas): ").strip())
    except ValueError:
        raise ValueError("La duraciÃ³n en horas debe ser un valor numÃ©rico.")

    reserva = crear_reserva(cliente_sel, servicio_sel, horas)
    print(f"âœ“ Reserva creada en estado '{reserva.estado}': {reserva}")
    registrar_evento(f"MenÃº: Reserva creada ({reserva})")

    procesar_ahora = input("Â¿Desea confirmar y procesar el pago ahora? (s/n): ").strip().lower()
    if procesar_ahora == "s":
        try:
            desc_porcentaje = float(input("Porcentaje de descuento (0 a 99, ej. 10 para 10%): ").strip() or "0")
        except ValueError:
            raise ValueError("El descuento debe ser un valor numÃ©rico.")

        descuento = desc_porcentaje / 100.0
        resumen_pago = confirmar_y_procesar(reserva, descuento=descuento)
        print(f"âœ“ {resumen_pago}")


def opcion_listar_registros():
    print("\n=== ESTADO ACTUAL DEL SISTEMA ===")
    print(f"\nClientes ({len(clientes)}):")
    if not clientes:
        print("  (Ninguno)")
    for c in clientes:
        print(f"  - {c}")

    print(f"\nServicios ({len(servicios)}):")
    if not servicios:
        print("  (Ninguno)")
    for s in servicios:
        disp = "Disponible" if s.disponible else "No disponible"
        print(f"  - {s} [{disp}]")

    print(f"\nReservas ({len(reservas)}):")
    if not reservas:
        print("  (Ninguna)")
    for r in reservas:
        costo_str = f" | Costo: ${r.costo:,.2f}" if r.costo is not None else ""
        print(f"  - {r}{costo_str}")


# ---------- SimulaciÃ³n automÃ¡tica original ----------
def ejecutar_simulacion(numero, descripcion, funcion):
    print(f"\nOperaciÃ³n {numero}: {descripcion}")
    try:
        resultado = funcion()
    except SoftwareFJError as e:
        print(f"   âœ— Error controlado: {e}")
        if e.__cause__:
            print(f"     Causa original: {e.__cause__}")
        registrar_error(f"Op {numero} ({descripcion}): {e}")
    except Exception as e:
        print(f"   âœ— Error inesperado: {type(e).__name__}: {e}")
        registrar_error(f"Op {numero} inesperado: {type(e).__name__}: {e}")
    else:
        print(f"   âœ“ OK: {resultado}")
        registrar_evento(f"Op {numero} ({descripcion}) exitosa")


def correr_simulacion_demo():
    registrar_evento("===== Inicio de la simulaciÃ³n automÃ¡tica =====")
    print("\n=== EJECUTANDO SIMULACIÃ“N DE 17 OPERACIONES ===")

    ejecutar_simulacion(1, "Registrar cliente vÃ¡lido",
                        lambda: crear_cliente("Ana Gomez", "1012345678", "ana@correo.com", "3001234567"))
    ejecutar_simulacion(2, "Registrar cliente con correo invÃ¡lido",
                        lambda: crear_cliente("Pedro Ruiz", "1098765432", "pedro-correo", "3109876543"))
    ejecutar_simulacion(3, "Registrar cliente con documento con letras",
                        lambda: crear_cliente("Laura Diaz", "ABC123", "laura@correo.com", "3201112233"))
    ejecutar_simulacion(4, "Registrar segundo cliente vÃ¡lido",
                        lambda: crear_cliente("Carlos Perez", "79123456", "carlos@empresa.co", "3157778899"))

    ejecutar_simulacion(5, "Crear sala de reuniones vÃ¡lida",
                        lambda: crear_servicio(ReservaSala, "Sala Andes", 50000, 25))
    ejecutar_simulacion(6, "Crear sala con capacidad imposible (0)",
                        lambda: crear_servicio(ReservaSala, "Sala Fantasma", 40000, 0))
    ejecutar_simulacion(7, "Crear alquiler de equipos vÃ¡lido",
                        lambda: crear_servicio(AlquilerEquipo, "PortÃ¡til", 15000, 3))
    ejecutar_simulacion(8, "Crear asesorÃ­a con nivel inexistente",
                        lambda: crear_servicio(Asesoria, "AsesorÃ­a Python", 80000, "master"))
    ejecutar_simulacion(9, "Crear asesorÃ­a vÃ¡lida",
                        lambda: crear_servicio(Asesoria, "AsesorÃ­a Python", 80000, "experto"))
    ejecutar_simulacion(10, "Crear servicio con tarifa negativa",
                        lambda: crear_servicio(AlquilerEquipo, "Proyector", -5000, 1))

    ana, carlos = clientes[-2], clientes[-1]
    sala, portatiles, asesoria = servicios[-3], servicios[-2], servicios[-1]
    r1 = None

    def reserva_exitosa():
        nonlocal r1
        r1 = crear_reserva(ana, sala, 3)
        return confirmar_y_procesar(r1)

    ejecutar_simulacion(11, "Reserva exitosa de sala (3 h)", reserva_exitosa)
    ejecutar_simulacion(12, "Reserva con duraciÃ³n negativa",
                        lambda: crear_reserva(carlos, portatiles, -2))

    def reservar_no_disponible():
        asesoria.cambiar_disponibilidad(False)
        return crear_reserva(carlos, asesoria, 2)

    ejecutar_simulacion(13, "Reservar asesorÃ­a no disponible", reservar_no_disponible)
    ejecutar_simulacion(14, "Cancelar una reserva ya procesada", lambda: r1.cancelar())

    def descuento_invalido():
        r = crear_reserva(carlos, portatiles, 4)
        return confirmar_y_procesar(r, descuento=1.5)

    ejecutar_simulacion(15, "Procesar con descuento imposible (encadenamiento)", descuento_invalido)

    def reserva_con_descuento():
        r = crear_reserva(carlos, portatiles, 4)
        return confirmar_y_procesar(r, descuento=0.10)

    ejecutar_simulacion(16, "Reserva exitosa con 10 % de descuento", reserva_con_descuento)
    ejecutar_simulacion(17, "Reserva sin cliente (dato faltante)",
                        lambda: crear_reserva(None, sala, 1))

    print(f"\nSimulaciÃ³n finalizada. Registros guardados en '{ARCHIVO_LOG}'.")


# ---------- Bucle principal del menÃº ----------
def main():
    registrar_evento("===== Inicio del sistema interactivo Software FJ =====")
    while True:
        print("\n=========================================")
        print("       SISTEMA SOFTWARE FJ - MENÃš")
        print("=========================================")
        print("  1. Registrar cliente")
        print("  2. Crear servicio")
        print("  3. Hacer reserva")
        print("  4. Listar clientes, servicios y reservas")
        print("  5. Ejecutar simulaciÃ³n automÃ¡tica (17 casos)")
        print("  0. Salir")
        print("=========================================")

        opcion = input("Seleccione una opciÃ³n: ").strip()

        try:
            if opcion == "1":
                opcion_registrar_cliente()
            elif opcion == "2":
                opcion_crear_servicio()
            elif opcion == "3":
                opcion_hacer_reserva()
            elif opcion == "4":
                opcion_listar_registros()
            elif opcion == "5":
                correr_simulacion_demo()
            elif opcion == "0":
                print("\nSaliendo del sistema. Â¡Hasta luego!")
                registrar_evento("===== Fin de sesiÃ³n interactiva =====")
                break
            else:
                print("\nâš  OpciÃ³n no vÃ¡lida. Por favor ingrese un nÃºmero del 0 al 5.")

        except SoftwareFJError as e:
            print(f"\nâœ— Error de validaciÃ³n del sistema: {e}")
            if e.__cause__:
                print(f"  Causa original: {e.__cause__}")
            registrar_error(f"MenÃº - Error de negocio: {e}")

        except ValueError as e:
            print(f"\nâœ— Error de entrada por teclado: {e}")
            registrar_error(f"MenÃº - Entrada invÃ¡lida: {e}")

        except KeyboardInterrupt:
            print("\n\nInterrupciÃ³n detectada. Cerrando el programa de forma segura...")
            break

        except Exception as e:
            print(f"\nâœ— Error inesperado: {type(e).__name__}: {e}")
            registrar_error(f"MenÃº - Error inesperado: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
