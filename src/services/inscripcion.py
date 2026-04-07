from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.inscripcion import Inscripcion  
from src.entities.inscripcion import EstadoInscripcion
from src.services import curso as curso_services
from src.entities.certificado import Certificado  


def obtener_inscripcion_activa(
    db: Session, id_usuario_inscrito: UUID, id_curso: UUID
) -> Optional[Inscripcion]:
    return (
        db.query(Inscripcion)
        .filter(
            Inscripcion.id_usuario_inscrito == id_usuario_inscrito,
            Inscripcion.id_curso == id_curso,
            Inscripcion.estado_inscripcion == EstadoInscripcion.ACTIVA,
        )
        .first()
    )

def crear(
    db: Session,
    id_curso: UUID,
    id_usuario_inscrito: UUID,
    id_usuario_creacion: UUID,
    estado_inscripcion: str = None
    ) -> Inscripcion:
    if estado_inscripcion is None:
        estado_inscripcion = EstadoInscripcion.PENDIENTE.value

    curso = curso_services.obtener_por_id(db, id_curso)
    if not curso:
        raise ValueError("El curso no existe")
    
    existente_inscripcion = obtener_inscripcion_activa(db, id_usuario_inscrito, id_curso)
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

def obtener_por_id(db: Session, id_inscripcion: UUID) -> Optional[Inscripcion]:
    return (
        db.query(Inscripcion)
        .filter(Inscripcion.id_inscripcion == id_inscripcion)
        .first()
    )

def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Inscripcion]:
    return db.query(Inscripcion).offset(skip).limit(limit).all()

def obtener_por_usuario(db: Session, id_usuario: UUID) -> List[Inscripcion]:
    return (
        db.query(Inscripcion)
        .filter(Inscripcion.id_usuario_inscrito == id_usuario)
        .all()
    )

def actualizar(
    db: Session,
    id_inscripcion: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Inscripcion]:
    insc = obtener_por_id(
        db, id_inscripcion
    )  
    if not insc:
        return None
    for key, value in kwargs.items():
        if hasattr(insc, key):
            setattr(insc, key, value)
    insc.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(insc)
    return insc

def eliminar(db: Session, id_inscripcion: UUID) -> bool:
    certificado = db.query(Certificado).filter(
        Certificado.id_inscripcion == id_inscripcion
    ).first()

    if certificado:
        raise ValueError("No se puede eliminar la inscripción porque tiene un certificado asociado")
    
    inscripcion = obtener_por_id(db, id_inscripcion)
    if not inscripcion:
        return False
    db.delete(inscripcion)
    db.commit()
    return True

def obtener_por_usuario_y_curso(
    db: Session, id_usuario: UUID, id_curso: UUID
) -> Optional[Inscripcion]:
    return (
        db.query(Inscripcion)
        .filter(
            Inscripcion.id_usuario_inscrito == id_usuario,
            Inscripcion.id_curso == id_curso,
        )
        .first()
    )

