from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.Leccion import Leccion

db = SessionLocal()


def crear(
    Id_leccion: UUID,
    id_usuario_creacion: UUID,
    id_curso: UUID,
    titulo_leccion: str,
    descripcion_leccion: str,
    orden: int,
    duracion_horas: int,
) -> Leccion:
    leccion = Leccion(
        id_leccion=Id_leccion,
        id_usuario_creacion=id_usuario_creacion,
        id_curso=id_curso,
        titulo_leccion=titulo_leccion,
        descripcion_leccion=descripcion_leccion,
        orden=orden,
        duracion_horas=duracion_horas,
    )
    db.add(leccion)
    db.commit()
    db.refresh(leccion)
    return leccion


def obtener_por_id(id_leccion: UUID) -> Optional[Leccion]:
    return db.query(Leccion).filter(Leccion.id_leccion == id_leccion).first()


def obtener_todos() -> List[Leccion]:
    return db.query(Leccion).all()


def obtener_por_usuario(id_usuario: UUID) -> List[Leccion]:
    return db.query(Leccion).filter(Leccion.id_usuario == id_usuario).all()


def actualizar(
    id_leccion: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Leccion]:
    leccion = obtener_por_id(id_leccion)
    if not leccion:
        return None
    for key, value in kwargs.items():
        if hasattr(leccion, key):
            setattr(leccion, key, value)
    leccion.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(leccion)
    return leccion


def eliminar(id_leccion: UUID) -> bool:
    leccion = obtener_por_id(id_leccion)
    if not leccion:
        return False
    db.delete(leccion)
    db.commit()
    return True
