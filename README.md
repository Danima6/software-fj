# Software FJ – Sistema de Gestión de Clientes, Servicios y Reservas

Proyecto de la **Fase 4 – Componente práctico** del curso Programación (213023), UNAD.
Grupo **213023_224**.

Sistema orientado a objetos, **sin base de datos**, con manejo avanzado de excepciones.
Toda la información se guarda en listas de objetos y los eventos/errores en `software_fj.log`.

## Cómo ejecutarlo

```bash
python main.py
```

Requiere Python 3.8 o superior. No necesita librerías externas.

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (todas heredan de `SoftwareFJError`) |
| `registro.py` | Configuración del archivo de logs |
| `entidad.py` | Clase abstracta `Entidad` (base de todo el sistema) |
| `cliente.py` | Clase `Cliente` con encapsulación y validaciones |
| `servicios.py` | Clase abstracta `Servicio` + `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | Clase `Reserva` (confirmar, cancelar, procesar) |
| `main.py` | Simulación de 17 operaciones válidas e inválidas |

## Requisitos del Anexo 3 y dónde se cumplen

- **Clase abstracta general** → `Entidad` (`entidad.py`)
- **Cliente con validaciones y encapsulación** → atributos privados `__nombre`, `__documento`, etc. (`cliente.py`)
- **Servicio abstracto + 3 servicios con polimorfismo** → `costo_base()`, `describir()`, `validar_parametros()` sobrescritos (`servicios.py`)
- **Reserva con confirmación, cancelación y procesamiento** → `reserva.py`
- **Métodos sobrecargados** → `calcular_costo(horas, con_iva=False, descuento=0.0)`
- **Excepciones personalizadas** → `excepciones.py`
- **try/except, try/except/else, try/except/finally** → `Reserva.procesar()` y `ejecutar()` en `main.py`
- **Encadenamiento de excepciones** → `raise ReservaInvalidaError(...) from e` en `Reserva.procesar()`
- **Archivo de logs** → `software_fj.log`
- **Mínimo 10 operaciones** → `main.py` simula 17

## Flujo de trabajo

Cada módulo se desarrolla en su propia rama (`feature/cliente`, `feature/servicios`, `feature/reserva`, `feature/main`) y se integra a `main` mediante un *pull request*. Las mejoras pendientes están en la pestaña **Issues**.

## Integrantes

- Daniel Esteban Macías Holguín
- Luis Alberto Dueñas Mosquera
