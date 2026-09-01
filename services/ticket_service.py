from __future__ import annotations

from models.ticket import Ticket
from services.usuario_service import UsuarioService


class TicketService:
    def __init__(self, usuario_service: UsuarioService) -> None:
        self.__tickets: list[Ticket] = []
        self.__contador: int = 1
        self.__usuario_service = usuario_service

    def registrar(
        self,
        id_usuario: int,
        titulo: str,
        descripcion: str,
        categoria: str,
        prioridad: str,
    ) -> Ticket:
       
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
        
        return list(self.__tickets)

    def listar_por_usuario(self, id_usuario: int) -> list[Ticket]:

        return [
            ticket
            for ticket in self.__tickets
            if ticket.obtener_solicitante().obtener_id() == id_usuario
        ]

    def buscar_por_id(self, id: int) -> "Ticket | None":
        
        for ticket in self.__tickets:
            if ticket.obtener_id() == id:
                return ticket
        return None

    def cambiar_estado(self, id: int, estado: str) -> bool:
        
        ticket = self.buscar_por_id(id)
        if ticket is None:
            return False
        ticket.cambiar_estado(estado)
        return True

    def cambiar_prioridad(self, id: int, prioridad: str) -> bool:
        
        ticket = self.buscar_por_id(id)
        if ticket is None:
            return False
        ticket.cambiar_prioridad(prioridad)
        return True

    # ------------------------------------------------------------------
    # Extension Semana 9: asignacion de tecnico
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


    def listar_por_tecnico(self, id_tecnico: int) -> list[Ticket]:
        
        return [
            ticket
            for ticket in self.__tickets
            if ticket.obtener_tecnico_asignado() is not None
            and ticket.obtener_tecnico_asignado().obtener_id() == id_tecnico
        ]

    def listar_por_categoria(self, categoria: str) -> list[Ticket]:
        
        return [
            ticket
            for ticket in self.__tickets
            if ticket.obtener_categoria().strip().lower() == categoria.strip().lower()
        ]

    def listar_por_estado(self, estado: str) -> list[Ticket]:
        
        estado_normalizado = estado.strip().upper()
        if estado_normalizado not in Ticket.ESTADOS:
            raise ValueError(f"Estado de ticket invalido: {estado!r}")

        return [
            ticket
            for ticket in self.__tickets
            if ticket.obtener_estado() == estado_normalizado
        ]
