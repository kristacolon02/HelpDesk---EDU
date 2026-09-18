"""
Módulo de registro de incidencias en memoria - HelpDesk EDU
Universidad Mariano Gálvez de Guatemala
Programación II

"""

from abc import ABC, abstractmethod
from datetime import datetime


class RegistroIncidenciasError(Exception):
    """Excepción base del módulo: permite capturar cualquier error propio con un solo except."""


class IncidenciaNoEncontradaError(RegistroIncidenciasError):

    def __init__(self, id_incidencia: int) -> None:
        super().__init__(f"No existe una incidencia con el id {id_incidencia}.")
        self.id_incidencia = id_incidencia


class EstadoInvalidoError(RegistroIncidenciasError):

    def __init__(self, estado_recibido: str, estados_validos: tuple[str, ...]) -> None:
        super().__init__(
            f"El estado '{estado_recibido}' no es válido. "
            f"Estados permitidos: {', '.join(estados_validos)}."
        )
        self.estado_recibido = estado_recibido
        self.estados_validos = estados_validos


class Incidencia:

    ESTADOS_VALIDOS: tuple[str, ...] = ("Abierta", "En progreso", "Resuelta", "Cerrada")

    def __init__(
        self,
        id_incidencia: int,
        titulo: str,
        descripcion: str,
        categoria: str,
        prioridad: str,
        estado: str = "Abierta",
    ) -> None:
        self._id = id_incidencia
        self._titulo = titulo
        self._descripcion = descripcion
        self._categoria = categoria
        self._prioridad = prioridad
        self._fecha_creacion = datetime.now()
        self._estado = ""
        # Se asigna por medio del setter para que el estado inicial también se valide.
        self.estado = estado

    @property
    def id(self) -> int:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def categoria(self) -> str:
        return self._categoria

    @property
    def prioridad(self) -> str:
        return self._prioridad

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: str) -> None:
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise EstadoInvalidoError(nuevo_estado, self.ESTADOS_VALIDOS)
        self._estado = nuevo_estado

    def __str__(self) -> str:
        return (
            f"[{self._id}] {self._titulo} | Categoría: {self._categoria} | "
            f"Prioridad: {self._prioridad} | Estado: {self._estado} | "
            f"Creada: {self._fecha_creacion:%d/%m/%Y %H:%M:%S}"
        )

    def __repr__(self) -> str:
        return f"Incidencia(id={self._id}, titulo={self._titulo!r}, estado={self._estado!r})"


class CanalNotificacion(ABC):

    @abstractmethod
    def notificar(self, mensaje: str) -> None:
        """Envía el mensaje por el canal concreto que implemente esta clase."""


class NotificacionConsola(CanalNotificacion):

    def notificar(self, mensaje: str) -> None:
        print(f"[consola] >>> {mensaje}")


class NotificacionEmailSimulado(CanalNotificacion):

    def __init__(self, destinatario: str = "soporte@helpdeskedu.edu.gt") -> None:
        self._destinatario = destinatario
        self._bandeja_enviados: list[str] = []

    @property
    def destinatario(self) -> str:
        return self._destinatario

    @property
    def bandeja_enviados(self) -> tuple[str, ...]:
        return tuple(self._bandeja_enviados)

    def notificar(self, mensaje: str) -> None:
        correo = f"Para: {self._destinatario} | Asunto: HelpDesk EDU | Cuerpo: {mensaje}"
        self._bandeja_enviados.append(correo)
        print(f"[email simulado] {correo}")


class GestorIncidencias:

    def __init__(self) -> None:
        self._incidencias: dict[int, Incidencia] = {}
        self._ultimo_id = 0

    def crear_incidencia(
        self, titulo: str, descripcion: str, categoria: str, prioridad: str
    ) -> Incidencia:
        self._ultimo_id += 1
        incidencia = Incidencia(
            id_incidencia=self._ultimo_id,
            titulo=titulo,
            descripcion=descripcion,
            categoria=categoria,
            prioridad=prioridad,
            estado="Abierta",
        )
        self._incidencias[incidencia.id] = incidencia
        return incidencia

    def listar_incidencias(self) -> list[Incidencia]:
        # Se devuelve una lista nueva para no exponer la colección interna.
        return list(self._incidencias.values())

    def buscar_por_id(self, id_incidencia: int) -> Incidencia:
        if id_incidencia not in self._incidencias:
            raise IncidenciaNoEncontradaError(id_incidencia)
        return self._incidencias[id_incidencia]

    def cambiar_estado(self, id_incidencia: int, nuevo_estado: str) -> None:
        incidencia = self.buscar_por_id(id_incidencia)
        # EstadoInvalidoError se deja propagar hacia quien invoca el método.
        incidencia.estado = nuevo_estado

    def eliminar_incidencia(self, id_incidencia: int) -> None:
        if id_incidencia not in self._incidencias:
            raise IncidenciaNoEncontradaError(id_incidencia)
        del self._incidencias[id_incidencia]

    def total_incidencias(self) -> int:
        return len(self._incidencias)


def _separador(titulo: str) -> None:
    print(f"\n{'=' * 70}\n{titulo}\n{'=' * 70}")


if __name__ == "__main__":
    gestor = GestorIncidencias()
    canales: list[CanalNotificacion] = [NotificacionConsola(), NotificacionEmailSimulado()]

    _separador("1. REGISTRO DE INCIDENCIAS")
    incidencia_1 = gestor.crear_incidencia(
        titulo="No carga la plataforma virtual",
        descripcion="Los estudiantes reportan error 500 al ingresar al aula virtual.",
        categoria="Software",
        prioridad="Alta",
    )
    incidencia_2 = gestor.crear_incidencia(
        titulo="Impresora del laboratorio sin red",
        descripcion="La impresora del laboratorio 3 no aparece en la red institucional.",
        categoria="Hardware",
        prioridad="Media",
    )
    for incidencia in gestor.listar_incidencias():
        print(incidencia)

    _separador("2. CAMBIO DE ESTADO CON UN VALOR VÁLIDO")
    gestor.cambiar_estado(incidencia_1.id, "En progreso")
    print(gestor.buscar_por_id(incidencia_1.id))

    _separador("3. CAMBIO DE ESTADO CON UN VALOR INVÁLIDO")
    try:
        gestor.cambiar_estado(incidencia_2.id, "Pendiente")
    except EstadoInvalidoError as error:
        print(f"No se pudo cambiar el estado -> {error}")
        print(f"La incidencia conserva su estado: {gestor.buscar_por_id(incidencia_2.id).estado}")

    _separador("4. NOTIFICACIÓN POLIMÓRFICA POR TODOS LOS CANALES")
    mensaje = (
        f"Se registró la incidencia {incidencia_1.id}: '{incidencia_1.titulo}' "
        f"(prioridad {incidencia_1.prioridad}, estado {incidencia_1.estado})."
    )
    for canal in canales:
        canal.notificar(mensaje)

    _separador("5. BÚSQUEDA DE UNA INCIDENCIA INEXISTENTE")
    try:
        gestor.buscar_por_id(99)
    except IncidenciaNoEncontradaError as error:
        print(f"Búsqueda fallida -> {error}")

    _separador("6. ELIMINACIÓN DE UNA INCIDENCIA")
    gestor.eliminar_incidencia(incidencia_2.id)
    print(f"Incidencias restantes: {gestor.total_incidencias()}")
    for incidencia in gestor.listar_incidencias():
        print(incidencia)
