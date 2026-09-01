"""Pruebas de las consultas del sistema HelpDesk EDU (week09).
"""

from services.usuario_service import UsuarioService
from services.ticket_service import TicketService


def crear_servicios():
    
    usuario_service = UsuarioService()
    ticket_service = TicketService(usuario_service)
    return usuario_service, ticket_service


def crear_ticket(ticket_service, id_usuario, titulo, categoria, prioridad="MEDIUM"):
    return ticket_service.registrar(
        id_usuario=id_usuario,
        titulo=titulo,
        descripcion="Caso de prueba",
        categoria=categoria,
        prioridad=prioridad,
    )


# --------------------------------------------------------------------
# listar_por_tecnico
# --------------------------------------------------------------------

def test_listar_por_tecnico_retorna_solo_tickets_asignados():
    usuario_service, ticket_service = crear_servicios()
    solicitante = usuario_service.registrar("Ana Lopez", "ana@edu.gt", "REQUESTER")
    tecnico_1 = usuario_service.registrar("Luis Tec", "luis@edu.gt", "TECHNICIAN")
    tecnico_2 = usuario_service.registrar("Marta Tec", "marta@edu.gt", "TECHNICIAN")

    primero = crear_ticket(ticket_service, solicitante.obtener_id(), "No imprime", "Hardware")
    segundo = crear_ticket(ticket_service, solicitante.obtener_id(), "No ingresa", "Software")

    ticket_service.asignar_tecnico(primero.obtener_id(), tecnico_1.obtener_id())
    ticket_service.asignar_tecnico(segundo.obtener_id(), tecnico_2.obtener_id())

    resultado = ticket_service.listar_por_tecnico(tecnico_1.obtener_id())

    assert resultado == [primero]


def test_listar_por_tecnico_retorna_vacio_si_no_hay_asignacion():
    usuario_service, ticket_service = crear_servicios()
    solicitante = usuario_service.registrar("Ana Lopez", "ana@edu.gt", "REQUESTER")
    crear_ticket(ticket_service, solicitante.obtener_id(), "No imprime", "Hardware")

    resultado = ticket_service.listar_por_tecnico(999)

    assert resultado == []


# --------------------------------------------------------------------
# listar_por_categoria
# --------------------------------------------------------------------

def test_listar_por_categoria_retorna_solo_categoria_correcta():
    usuario_service, ticket_service = crear_servicios()
    solicitante = usuario_service.registrar("Ana Lopez", "ana@edu.gt", "REQUESTER")

    hardware = crear_ticket(ticket_service, solicitante.obtener_id(), "No imprime", "Hardware")
    crear_ticket(ticket_service, solicitante.obtener_id(), "No ingresa", "Software")

    resultado = ticket_service.listar_por_categoria("Hardware")

    assert resultado == [hardware]


def test_listar_por_categoria_no_distingue_mayusculas():
    usuario_service, ticket_service = crear_servicios()
    solicitante = usuario_service.registrar("Ana Lopez", "ana@edu.gt", "REQUESTER")
    hardware = crear_ticket(ticket_service, solicitante.obtener_id(), "No imprime", "Hardware")

    resultado = ticket_service.listar_por_categoria("hardware")

    assert resultado == [hardware]


# --------------------------------------------------------------------
# listar_por_estado
# --------------------------------------------------------------------

def test_listar_por_estado_retorna_solo_estado_correcto():
    usuario_service, ticket_service = crear_servicios()
    solicitante = usuario_service.registrar("Ana Lopez", "ana@edu.gt", "REQUESTER")
    abierto = crear_ticket(ticket_service, solicitante.obtener_id(), "Caso abierto", "General")

    resultado = ticket_service.listar_por_estado("open")

    assert abierto in resultado


def test_listar_por_estado_excluye_otros_estados():
    usuario_service, ticket_service = crear_servicios()
    solicitante = usuario_service.registrar("Ana Lopez", "ana@edu.gt", "REQUESTER")
    abierto = crear_ticket(ticket_service, solicitante.obtener_id(), "Caso abierto", "General")
    cerrado = crear_ticket(ticket_service, solicitante.obtener_id(), "Caso cerrado", "General")
    ticket_service.cambiar_estado(cerrado.obtener_id(), "CLOSED")

    resultado = ticket_service.listar_por_estado("OPEN")

    assert abierto in resultado
    assert cerrado not in resultado


def test_listar_por_estado_invalido_lanza_error():
    _, ticket_service = crear_servicios()

    try:
        ticket_service.listar_por_estado("no_existe")
        assert False, "Se esperaba un ValueError para un estado invalido"
    except ValueError:
        pass
