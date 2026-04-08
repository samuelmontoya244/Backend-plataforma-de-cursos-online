from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.Leccion import Leccion
from src.entities.Curso import Curso
from src.services import curso as curso_services




def crear(
    db: Session,
    id_usuario_creacion: UUID,
    id_curso: UUID,
    titulo_leccion: str = None,
    descripcion_leccion: str = None,
    orden: int = None,
    duracion_horas: int = None,
) -> Leccion:
    
    curso = curso_services.obtener_por_id(db, id_curso)
    if not curso:
        raise ValueError("El curso no existe")
    
    existente_leccion = obtener_por_orden_y_curso(db, orden, id_curso)
    if existente_leccion:
        raise ValueError("Ya existe una lección con este orden en el curso")
    
    nueva_leccion = Leccion(
        
        id_usuario_creacion=id_usuario_creacion,
        id_curso=id_curso,
        titulo_leccion=titulo_leccion,
        descripcion_leccion=descripcion_leccion,
        orden=orden,
        duracion_horas=duracion_horas,
    )
    db.add(nueva_leccion)
    db.commit()
    db.refresh(nueva_leccion)
    return nueva_leccion


def obtener_por_id(db: Session, id_leccion: UUID) -> Optional[Leccion]:
    return (
        db.query(Leccion)
        .filter(Leccion.id_leccion == id_leccion)
        .first()
    )

def obtener_todos(db: Session, skip: int = 0, limit: int = 100)-> List[Leccion]:
    return db.query(Leccion).offset(skip).limit(limit).all()


def obtener_por_usuario(db: Session, id_usuario: UUID) -> List[Leccion]:
    return (
        db.query(Leccion)
        .filter(Leccion.id_usuario == id_usuario)
        .all()
    )    


def actualizar(
    db: Session,
    id_leccion: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Leccion]:
    leccion = obtener_por_id(
        db, id_leccion
    )
    if not leccion:
        return None
    for key, value in kwargs.items():
        if hasattr(leccion, key):
            setattr(leccion, key, value)
    leccion.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(leccion)
    return leccion


def eliminar(db: Session, id_leccion: UUID) -> bool:
    leccion = obtener_por_id(db, id_leccion)
    if not leccion:
        return False
    db.delete(leccion)
    db.commit()
    return True

def obtener_por_orden_y_curso(db: Session, orden: int, id_curso: UUID) -> Optional[Leccion]:
    return (
        db.query(Leccion)
        .filter(
            Leccion.orden == orden,
            Leccion.id_curso == id_curso
        )
        .first()
    )
