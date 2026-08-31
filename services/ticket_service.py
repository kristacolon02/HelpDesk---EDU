"""Servicio de tickets: RF-07 a RF-13, mas las consultas de la Semana 9.

RF-09 se cumple aqui: antes de crear un Ticket se consulta al
UsuarioService; si el solicitante no existe, se rechaza el alta.
"""

from __future__ import annotations

from models.ticket import Ticket
from services.usuario_service import UsuarioService


class TicketService:
    def __init__(self, usuario_service: UsuarioService) -> None:
        self.__tickets: list[Ticket] = []
        self.__contador: int = 1
        self.__usuario_service = usuario_service

    # ------------------------------------------------------------------
    # Metodos base (Semana 7-8): RF-07 a RF-13
    # ------------------------------------------------------------------

    def registrar(
        self,
        id_usuario: int,
        titulo: str,
        descripcion: str,
        categoria: str,
        prioridad: str,
    ) -> Ticket:
        """RF-07/RF-08/RF-09: crea el ticket si el solicitante existe.

        El id, el estado inicial OPEN y la fecha de creacion se generan
        automaticamente dentro de la clase Ticket (RF-08).
        """
        solicitante = self.__usuario_service.buscar_por_id(id_usuario)
        if solicitante is None:
            raise ValueError(
                f"No se puede registrar el ticket: usuario {id_usuario} inexistente."
            )

        ticket = Ticket(
            id=self.__contador,
            solicitante=solicitante,
            titulo=titulo,
            descripcion=descripcion,
            categoria=categoria,
            prioridad=prioridad,
        )
        self.__tickets.append(ticket)
        self.__contador += 1
        return ticket

    def listar(self) -> list[Ticket]:
        """RF-10: lista todos los tickets."""
        return list(self.__tickets)

    def listar_por_usuario(self, id_usuario: int) -> list[Ticket]:
        """RF-10: filtra los tickets de un solicitante especifico."""
        return [
            ticket
            for ticket in self.__tickets
            if ticket.obtener_solicitante().obtener_id() == id_usuario
        ]

    def buscar_por_id(self, id: int) -> "Ticket | None":
        """RF-11: busca un ticket por ID, devuelve None si no existe."""
        for ticket in self.__tickets:
            if ticket.obtener_id() == id:
                return ticket
        return None

    def cambiar_estado(self, id: int, estado: str) -> bool:
        """RF-12: cambia el estado. Devuelve False si el ticket no existe."""
        ticket = self.buscar_por_id(id)
        if ticket is None:
            return False
        ticket.cambiar_estado(estado)
        return True

    def cambiar_prioridad(self, id: int, prioridad: str) -> bool:
        """RF-13: cambia la prioridad. Devuelve False si el ticket no existe."""
        ticket = self.buscar_por_id(id)
        if ticket is None:
            return False
        ticket.cambiar_prioridad(prioridad)
        return True

    # ------------------------------------------------------------------
    # Extension Semana 9: asignacion de tecnico (necesaria para poder
    # filtrar por tecnico). Debe agregarse al UML (RNF-09).
    # ------------------------------------------------------------------

    def asignar_tecnico(self, id_ticket: int, id_tecnico: int) -> bool:
        ticket = self.buscar_por_id(id_ticket)
        if ticket is None:
            return False
        tecnico = self.__usuario_service.buscar_por_id(id_tecnico)
        if tecnico is None:
            raise ValueError(f"No existe un tecnico con id {id_tecnico}.")
        ticket.asignar_tecnico(tecnico)
        return True

    # ------------------------------------------------------------------
    # Consultas de la Semana 9: cada metodo responde una pregunta del
    # negocio usando las relaciones ya existentes entre las entidades.
    # ------------------------------------------------------------------

    def listar_por_tecnico(self, id_tecnico: int) -> list[Ticket]:
        """Que tickets tiene asignados este tecnico?

        Filtra por el objeto Usuario guardado en __tecnico_asignado,
        que es la relacion tecnico <-> ticket agregada esta semana.
        """
        return [
            ticket
            for ticket in self.__tickets
            if ticket.obtener_tecnico_asignado() is not None
            and ticket.obtener_tecnico_asignado().obtener_id() == id_tecnico
        ]

    def listar_por_categoria(self, categoria: str) -> list[Ticket]:
        """Que tickets pertenecen a una categoria especifica (ej. Hardware)?

        Se compara sin distinguir mayusculas/minusculas para que
        "hardware" y "Hardware" no se traten como valores distintos.
        """
        return [
            ticket
            for ticket in self.__tickets
            if ticket.obtener_categoria().strip().lower() == categoria.strip().lower()
        ]

    def listar_por_estado(self, estado: str) -> list[Ticket]:
        """Que tickets siguen abiertos o en proceso?

        Normaliza el texto recibido (mayusculas, sin espacios extra) y
        valida que sea uno de los estados definidos en Ticket.ESTADOS,
        reutilizando la misma regla de negocio que cambiar_estado.
        """
        estado_normalizado = estado.strip().upper()
        if estado_normalizado not in Ticket.ESTADOS:
            raise ValueError(f"Estado de ticket invalido: {estado!r}")

        return [
            ticket
            for ticket in self.__tickets
            if ticket.obtener_estado() == estado_normalizado
        ]
