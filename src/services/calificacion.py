from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.calificacion import Calificacion
from src.entities.inscripcion import Inscripcion, EstadoInscripcion

def crear(
    db: Session,
    id_inscripcion: UUID,
    id_evaluacion: UUID,
    Nota: float,
    id_usuario_creacion: UUID,
) -> Calificacion:
    
    if not (0 <= Nota <= 5):
        raise ValueError("La Nota debe estar entre 0 y 5")

    existente = obtener_por_id(db, id_inscripcion, id_evaluacion)
    if existente:
        raise ValueError(
            "Ya existe una calificación para esta inscripción y evaluación."
        )

    calificacion = Calificacion(
        id_inscripcion=id_inscripcion,
        id_evaluacion=id_evaluacion,
        Nota=Nota,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(calificacion)
    db.commit()
    db.refresh(calificacion)

    return calificacion

def obtener_por_id(db,
    id_inscripcion: UUID, id_evaluacion: UUID
) -> Optional[Calificacion]:
    return (
        db.query(Calificacion)
        .filter(
            Calificacion.id_inscripcion == id_inscripcion,
            Calificacion.id_evaluacion == id_evaluacion,
        )
        .first()
    )

def obtener_todos(db, skip: int = 0, limit: int = 100) -> List[Calificacion]:
    return db.query(Calificacion).offset(skip).limit(limit).all()

def obtener_por_inscripcion(db, id_inscripcion: UUID) -> List[Calificacion]:
    return (
        db.query(Calificacion)
        .filter(Calificacion.id_inscripcion == id_inscripcion)
        .all()
    )

def actualizar(
    db: Session,
    id_inscripcion: UUID,
    id_evaluacion: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Calificacion]:
    calificacion = obtener_por_id(db, id_inscripcion, id_evaluacion)
    if not calificacion:
        return None

    if "Nota" in kwargs and not (0 <= kwargs["Nota"] <= 5):
        raise ValueError("La Nota debe estar entre 0 y 5.")

    for key, value in kwargs.items():
        if hasattr(calificacion, key):
            setattr(calificacion, key, value)
    calificacion.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(calificacion)

    return calificacion

def eliminar(db: Session, id_inscripcion: UUID, id_evaluacion: UUID) -> bool:
    calificacion = obtener_por_id(db, id_inscripcion, id_evaluacion)
    if not calificacion:
        return False
    db.delete(calificacion)
    db.commit()
    return True

