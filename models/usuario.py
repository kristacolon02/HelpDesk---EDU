from __future__ import annotations


class Usuario:
    """Representa a un solicitante, tecnico, supervisor o administrador."""

    ROLES = ["REQUESTER", "TECHNICIAN", "SUPERVISOR", "ADMINISTRATOR"]
    ESTADOS = ["ACTIVO", "INACTIVO"]

    def __init__(
        self,
        id: int,
        nombre: str,
        email: str,
        rol: str,
        estado: str = "ACTIVO",
    ) -> None:
        self.__id = id
        self.__nombre = nombre
        self.__email = email
        self.__rol = rol
        self.__estado = estado


    def obtener_id(self) -> int:
        return self.__id

    def obtener_nombre(self) -> str:
        return self.__nombre

    def obtener_email(self) -> str:
        return self.__email

    def obtener_rol(self) -> str:
        return self.__rol

    def obtener_estado(self) -> str:
        return self.__estado

    
    def cambiar_nombre(self, nombre: str) -> None:
        self.__nombre = nombre

    def cambiar_email(self, email: str) -> None:
        if not email:
            raise ValueError("El correo electronico no puede estar vacio.")
        self.__email = email

    def cambiar_rol(self, rol: str) -> None:
        if rol not in Usuario.ROLES:
            raise ValueError(f"Rol invalido: {rol!r}")
        self.__rol = rol

    def cambiar_estado(self, estado: str) -> None:
        if estado not in Usuario.ESTADOS:
            raise ValueError(f"Estado de usuario invalido: {estado!r}")
        self.__estado = estado

    def __str__(self) -> str:
        return (
            f"Usuario(id={self.__id}, nombre={self.__nombre!r}, "
            f"email={self.__email!r}, rol={self.__rol}, estado={self.__estado})"
        )
