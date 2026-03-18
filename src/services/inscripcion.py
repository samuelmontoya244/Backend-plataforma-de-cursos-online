from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.inscripcion import inscripcion
from src.entities.inscripcion import EstadoInscripcion
from src.services import curso_services

db = SessionLocal()

def obtener_inscripcion_activa(
    id_usuario_inscrito: UUID,
    id_curso: UUID
) -> Optional[inscripcion]:

    return db.query(inscripcion).filter(
        inscripcion.id_usuario_inscrito == id_usuario_inscrito,
        inscripcion.id_curso == id_curso,
        inscripcion.estado_inscripcion == EstadoInscripcion.ACTIVA
    ).first()

def crear(
    id_curso: UUID,
    id_usuario_inscrito: UUID,
    estado_inscripcion: str,
    id_usuario_creacion: UUID) -> inscripcion:

    curso = curso_services.obtener_por_id(id_curso)
    if not curso:
        raise ValueError("El curso no existe")
    
    existente_inscripcion = obtener_inscripcion_activa(id_usuario_inscrito, id_curso)
    if existente_inscripcion:
        raise ValueError("El usuario ya está inscrito en este curso")
    
    nueva_inscripcion = inscripcion(
        id_curso=id_curso,
        id_usuario_inscrito=id_usuario_inscrito,
        estado_inscripcion=EstadoInscripcion.ACTIVA,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(nueva_inscripcion)
    db.commit()
    db.refresh(nueva_inscripcion)
    return nueva_inscripcion

def obtener_por_id(id_inscripcion: UUID) -> Optional[inscripcion]:
    return db.query(inscripcion).filter(inscripcion.id_inscripcion == id_inscripcion).first()

def obtener_todos() -> List[inscripcion]:
    return db.query(inscripcion).all()

def obtener_por_usuario(id_usuario: UUID) -> List[inscripcion]:
    return db.query(inscripcion).filter(inscripcion.id_usuario_inscrito == id_usuario).all()

def actualizar(
    id_inscripcion: UUID,
    id_usuario_edita: UUID,
    
    **kwargs: dict,
) -> Optional[inscripcion]:
    inscripcion = obtener_por_id(id_inscripcion)
    if not inscripcion:
        return None
    for key, value in kwargs.items():
        if hasattr(inscripcion, key):
            setattr(inscripcion, key, value)
    inscripcion.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(inscripcion)
    return inscripcion


def eliminar(id_inscripcion: UUID) -> bool:
    inscripcion = obtener_por_id(id_inscripcion)
    if not inscripcion:
        return False
    db.delete(inscripcion)
    db.commit()
    return True