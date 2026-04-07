from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import usuario as services_usuario
from src.schemas.response_schema import RespuestaAPI
from src.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("", response_model=List[UsuarioResponse])
def listar_usuarios(db: DbSession, skip: int = 0, limit: int = 100):
    usuarios = services_usuario.obtener_todos(db, skip=skip, limit=limit)
    return usuarios

@router.get("/{id_usuario}", response_model=UsuarioResponse)
def obtener_usuario(db: DbSession, id_usuario: UUID) -> UsuarioResponse:
    db_usuario = services_usuario.obtener_por_id(db, id_usuario)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"El usuario con ID {id_usuario} no existe en la base de datos"
        )
    return db_usuario

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(db: DbSession, dato: UsuarioCreate):

    try:
        usuario = services_usuario.crear(
            db,
            nombre_usuario=dato.nombre_usuario,
            tipo_documento=dato.tipo_documento,
            documento_identidad=dato.documento_identidad,
            email=str(dato.email),
            contrasena=dato.contrasena,
            rol=dato.rol,
            activo=dato.activo,
        )
        return usuario

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(db: DbSession, id_usuario: UUID, dato: UsuarioUpdate):

    usuario = services_usuario.actualizar(
        db,
        id_usuario,
        **dato.model_dump(exclude_unset=True)
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario

@router.delete("/{id_usuario}", response_model=RespuestaAPI)
def eliminar_usuario(db: DbSession, id_usuario: UUID, ) -> None:
    try:
        # Verificar que el usuario existe
        usuario_existente = services_usuario.obtener_por_id(db, id_usuario)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        eliminado = services_usuario.eliminar(db, id_usuario)
        if eliminado:
            return RespuestaAPI(mensaje="Usuario eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar usuario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}",
        )
