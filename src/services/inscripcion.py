from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.inscripcion import Inscripcion
from src.entities.inscripcion import EstadoInscripcion
from src.services import curso as curso_services

db = SessionLocal()

def obtener_inscripcion_activa(
    id_usuario_inscrito: UUID,
    id_curso: UUID
) -> Optional[Inscripcion]:

    return db.query(Inscripcion).filter(
        Inscripcion.id_usuario_inscrito == id_usuario_inscrito,
        Inscripcion.id_curso == id_curso,
        Inscripcion.estado_inscripcion == EstadoInscripcion.ACTIVA
    ).first()

def crear(
    id_curso: UUID,
    id_usuario_inscrito: UUID,
    id_usuario_creacion: UUID,
    estado_inscripcion: str = None
    ) -> Inscripcion:
    if estado_inscripcion is None:
        estado_inscripcion = EstadoInscripcion.PENDIENTE.value

    curso = curso_services.obtener_por_id(id_curso)
    if not curso:
        raise ValueError("El curso no existe")
    
    existente_inscripcion = obtener_inscripcion_activa(id_usuario_inscrito, id_curso)
    if existente_inscripcion:
        raise ValueError("El usuario ya está inscrito en este curso")
    
    nueva_inscripcion = Inscripcion(
        id_curso=id_curso,
        id_usuario_inscrito=id_usuario_inscrito,
        estado_inscripcion=EstadoInscripcion.PENDIENTE,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(nueva_inscripcion)
    db.commit()
    db.refresh(nueva_inscripcion)
    return nueva_inscripcion

def obtener_por_id(id_inscripcion: UUID) -> Optional[Inscripcion]:
    return db.query(Inscripcion).filter(Inscripcion.id_inscripcion == id_inscripcion).first()

def obtener_todos() -> List[Inscripcion]:
    return db.query(Inscripcion).all()

def obtener_por_usuario(id_usuario: UUID) -> List[Inscripcion]:
    return db.query(Inscripcion).filter(Inscripcion.id_usuario_inscrito == id_usuario).all()

def obtener_por_usuario_y_curso(id_usuario, id_curso):
    return db.query(Inscripcion).filter(
        Inscripcion.id_usuario_inscrito == id_usuario,
        Inscripcion.id_curso == id_curso
    ).first()

def actualizar(
    id_inscripcion: UUID,
    id_usuario_edita: UUID,
    
    **kwargs: dict,
) -> Optional[Inscripcion]:
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
