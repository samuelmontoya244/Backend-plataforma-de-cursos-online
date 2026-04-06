from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from .deps import DbSession
from src.entities.usuario import Usuario
from src.database.config import get_db

from src.services import usuario as services_usuario
from schemas import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioRead,
    RespuestaUsuarios
)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=RespuestaUsuarios)
def listar_usuarios(db: DbSession = Depends(get_db)):
    usuarios = services_usuario.obtener_todos(db)
    return {
        "message": "Lista de usuarios obtenida",
        "data": usuarios
    }


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: UUID, db: DbSession = Depends(get_db)) -> UsuarioRead:
    db_usuario = services_usuario.obtener_por_id(db, id_usuario)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"El usuario con ID {id_usuario} no existe en la base de datos"
        )
    return db_usuario


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(dato: UsuarioCreate, db: DbSession = Depends(get_db)) -> UsuarioRead:
    if db.query(Usuario).filter(Usuario.email==dato.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")
    nuevo_usuario = Usuario(
        nombre_usuario=dato.nombre_usuario,
        tipo_documento=dato.tipo_documento,
        documento_identidad=dato.documento_identidad,
        email=str(dato.email),
        contrasena=dato.contrasena,
        rol=dato.rol,
        activo=dato.activo,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(id_usuario: UUID, dato: UsuarioUpdate, db: DbSession = Depends(get_db)):
    usuario = services_usuario.obtener_por_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    update = dato.model_dump(exclude_unset=True)
    if "contrasena" in update and update["contrasena"]:
        update["contrasena_hash"] = services_usuario.hash_password(update.pop("contrasena"))
    for k, v in update.items():
        setattr(usuario, k, v)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: UUID, db: DbSession = Depends(get_db)) -> None:
    usuario = services_usuario.obtener_por_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return None