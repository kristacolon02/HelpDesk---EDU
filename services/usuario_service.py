from __future__ import annotations

from models.usuario import Usuario


class UsuarioService:
    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []
        self.__contador: int = 1

    def registrar(
        self, nombre: str, email: str, rol: str, estado: str = "ACTIVO"
    ) -> Usuario:
        
        self.__validar(email, rol)
        usuario = Usuario(
            id=self.__contador, nombre=nombre, email=email, rol=rol, estado=estado
        )
        self.__usuarios.append(usuario)
        self.__contador += 1
        return usuario

    def listar(self) -> list[Usuario]:
        
        return list(self.__usuarios)

    def buscar_por_id(self, id: int) -> "Usuario | None":
        
        for usuario in self.__usuarios:
            if usuario.obtener_id() == id:
                return usuario
        return None

    def actualizar(
        self,
        id: int,
        nombre: "str | None" = None,
        email: "str | None" = None,
        rol: "str | None" = None,
        estado: "str | None" = None,
    ) -> bool:
        
        usuario = self.buscar_por_id(id)
        if usuario is None:
            return False

        if nombre is not None:
            usuario.cambiar_nombre(nombre)
        if email is not None:
            usuario.cambiar_email(email)
        if rol is not None:
            usuario.cambiar_rol(rol)
        if estado is not None:
            usuario.cambiar_estado(estado)
        return True

    def existe(self, id: int) -> bool:
        return self.buscar_por_id(id) is not None

    def __validar(self, email: str, rol: str) -> None:
        
        if not email:
            raise ValueError("El correo electronico no puede estar vacio.")
        if rol not in Usuario.ROLES:
            raise ValueError(f"Rol invalido: {rol!r}")
