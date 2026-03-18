from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.material import Material

db = SessionLocal()


def crear(
    id_usuario_creacion: UUID,
    id_leccion: UUID,
    titulo_material: str,
    tipo_material: str,
    URL_archivo: str,
) -> Material:
    material = Material(
        id_usuario_creacion=id_usuario_creacion,
        id_leccion=id_leccion,
        titulo_material=titulo_material,
        tipo_material=tipo_material,
        URL_archivo=URL_archivo,
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


def obtener_por_id(id_material: UUID) -> Optional[Material]:
    return db.query(Material).filter(Material.id_material == id_material).first()


def obtener_todos() -> List[Material]:
    return db.query(Material).all()


def obtener_por_usuario(id_usuario: UUID) -> List[Material]:
    return db.query(Material).filter(Material.id_usuario == id_usuario).all()


def actualizar(
    id_material: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Material]:
    material = obtener_por_id(id_material)
    if not material:
        return None
    for key, value in kwargs.items():
        if hasattr(material, key):
            setattr(material, key, value)
    material.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(material)
    return material


def eliminar(id_material: UUID) -> bool:
    material = obtener_por_id(id_material)
    if not material:
        return False
    db.delete(material)
    db.commit()
    return True
