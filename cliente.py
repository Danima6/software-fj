"""
cliente.py
Clase Cliente con datos encapsulados y validaciones estrictas.
"""

import re  # Expresiones regulares para validar el correo

from entidad import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):
    """Representa a un cliente de Software FJ."""

    def __init__(self, nombre, documento, correo, telefono):
        # Atributos privados (doble guion bajo = encapsulación)
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono
        self.validar()                  # Si algo está mal, se lanza la excepción aquí mismo
        super().__init__()              # Solo si es válido, recibe su ID desde Entidad

    # ---------- Getters (solo lectura) ----------
    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    # ---------- Setter con validación ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo):
        # Solo permite cambiar el teléfono si el nuevo es válido
        if not str(nuevo).isdigit() or len(str(nuevo)) != 10:
            raise ClienteInvalidoError(f"Teléfono inválido: {nuevo}")
        self.__telefono = nuevo

    # ---------- Validaciones ----------
    def validar(self):
        """Revisa que todos los datos del cliente sean correctos."""
        # El nombre no puede estar vacío y debe tener solo letras y espacios
        if not self.__nombre or not str(self.__nombre).replace(" ", "").isalpha():
            raise ClienteInvalidoError(f"Nombre inválido: '{self.__nombre}'")
        # El documento debe ser numérico y tener entre 6 y 10 dígitos
        if not str(self.__documento).isdigit() or not 6 <= len(str(self.__documento)) <= 10:
            raise ClienteInvalidoError(f"Documento inválido: '{self.__documento}'")
        # El correo debe tener el formato algo@algo.algo
        if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", str(self.__correo)):
            raise ClienteInvalidoError(f"Correo inválido: '{self.__correo}'")
        # El teléfono debe tener exactamente 10 dígitos
        if not str(self.__telefono).isdigit() or len(str(self.__telefono)) != 10:
            raise ClienteInvalidoError(f"Teléfono inválido: '{self.__telefono}'")

    def describir(self):
        return f"Cliente #{self.id}: {self.__nombre} (doc. {self.__documento})"
