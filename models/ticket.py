"""Clase de dominio Ticket.

Cumple RNF-02 (atributos privados, acceso via metodos publicos),
RF-07/RF-08 (creacion con id, estado OPEN y fecha automaticos) y
RF-12/RF-13 (cambio de estado y prioridad con validacion de dominio).

Extension Semana 9: se agrega __tecnico_asignado para poder responder
"que tickets tiene asignados este tecnico?" (list_by_technician). Esta
extension debe reflejarse en el diagrama de clases (RNF-09).
"""

from __future__ import annotations

from datetime import datetime

from models.usuario import Usuario


class Ticket:
    """Representa un ticket de soporte reportado por un Usuario."""

    ESTADOS = ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED", "CANCELLED"]
    PRIORIDADES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    def __init__(
        self,
        id: int,
        solicitante: Usuario,
        titulo: str,
        descripcion: str,
        categoria: str,
        prioridad: str,
    ) -> None:
        if prioridad not in Ticket.PRIORIDADES:
            raise ValueError(f"Prioridad invalida: {prioridad!r}")

        self.__id = id
        self.__solicitante = solicitante
        self.__titulo = titulo
        self.__descripcion = descripcion
        self.__categoria = categoria
        self.__prioridad = prioridad
        self.__estado = "OPEN"
        self.__fecha_creacion = datetime.now()
        self.__tecnico_asignado: Usuario | None = None

    # -- getters (obtener_*) --------------------------------------------
    def obtener_id(self) -> int:
        return self.__id

    def obtener_solicitante(self) -> Usuario:
        return self.__solicitante

    def obtener_titulo(self) -> str:
        return self.__titulo

    def obtener_descripcion(self) -> str:
        return self.__descripcion

    def obtener_categoria(self) -> str:
        return self.__categoria

    def obtener_estado(self) -> str:
        return self.__estado

    def obtener_prioridad(self) -> str:
        return self.__prioridad

    def obtener_fecha_creacion(self) -> datetime:
        return self.__fecha_creacion

    def obtener_tecnico_asignado(self) -> "Usuario | None":
        return self.__tecnico_asignado

    # -- comportamiento del ciclo de vida (RF-12 / RF-13) -----------------
    def cambiar_estado(self, estado: str) -> None:
        if estado not in Ticket.ESTADOS:
            raise ValueError(f"Estado de ticket invalido: {estado!r}")
        self.__estado = estado

    def cambiar_prioridad(self, prioridad: str) -> None:
        if prioridad not in Ticket.PRIORIDADES:
            raise ValueError(f"Prioridad invalida: {prioridad!r}")
        self.__prioridad = prioridad

    # -- extension Semana 9: asignacion de tecnico ------------------------
    def asignar_tecnico(self, tecnico: Usuario) -> None:
        if tecnico.obtener_rol() not in ("TECHNICIAN", "SUPERVISOR"):
            raise ValueError(
                "Solo un usuario con rol TECHNICIAN o SUPERVISOR "
                "puede ser asignado a un ticket."
            )
        self.__tecnico_asignado = tecnico

    def __str__(self) -> str:
        tecnico = (
            self.__tecnico_asignado.obtener_nombre()
            if self.__tecnico_asignado
            else "Sin asignar"
        )
        return (
            f"Ticket(id={self.__id}, titulo={self.__titulo!r}, "
            f"categoria={self.__categoria}, prioridad={self.__prioridad}, "
            f"estado={self.__estado}, tecnico={tecnico})"
        )
