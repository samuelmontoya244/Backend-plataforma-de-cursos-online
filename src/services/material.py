from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.Material import Material
from src.services import leccion as leccion_services




def crear(
    db: Session,
    id_usuario_creacion: UUID,
    id_leccion: UUID,
    titulo_material: str = None,
    tipo_material: str = None,
    URL_archivo: str = None,
) -> Material:
    
    leccion = leccion_services.obtener_por_id(db, id_leccion)
    if not leccion:
        raise ValueError("La lección no existe")
    
    

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


def obtener_por_id(db: Session, id_material: UUID) -> Optional[Material]:
    return (db.query(Material).filter(Material.id_material == id_material).first())


def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Material]:
    return db.query(Material).offset(skip).limit(limit).all()


def obtener_por_usuario(db: Session, id_usuario: UUID) -> List[Material]:
    return (db.query(Material).filter(Material.id_usuario == id_usuario).all())


def actualizar(
    db: Session,
    id_material: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Material]:
    material = obtener_por_id(db, id_material)
    if not material:
        return None
    for key, value in kwargs.items():
        if hasattr(material, key):
            setattr(material, key, value)
    material.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(material)
    return material


def eliminar(db: Session, id_material: UUID) -> bool:
    material = db.query(Material).filter(
        Material.id_material == id_material
    ).first()

    if material is None:
        raise ValueError("No se puede eliminar el material porque está asociado a una lección")
    
    material = obtener_por_id(db, id_material)

    if not material:
        return False
    db.delete(material)
    db.commit()
    return True
