from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.calificacion import Calificacion

db = SessionLocal()


def crear(
    id_inscripcion: UUID, id_evaluacion: UUID, nota: float, id_usuario_creacion: UUID
) -> Calificacion:
    existente = obtener_por_id(id_inscripcion, id_evaluacion)
    if existente:
        raise ValueError(
            "Ya existe una calificación para esta inscripción y evaluación"
        )

    calificacion = Calificacion(
        id_inscripcion=id_inscripcion,
        id_evaluacion=id_evaluacion,
        nota=nota,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(calificacion)
    db.commit()
    db.refresh(calificacion)
    return calificacion


def obtener_por_id(id_inscripcion: UUID, id_evaluacion: UUID) -> Optional[Calificacion]:
    return (
        db.query(Calificacion)
        .filter(
            Calificacion.id_inscripcion == id_inscripcion,
            Calificacion.id_evaluacion == id_evaluacion,
        )
        .first()
    )


def obtener_todos() -> List[Calificacion]:
    return db.query(Calificacion).all()


def actualizar(
    id_inscripcion: UUID, id_evaluacion: UUID, id_usuario_edita: UUID, **kwargs: dict
) -> Optional[Calificacion]:
    calificacion = obtener_por_id(id_inscripcion, id_evaluacion)
    if not calificacion:
        return None
    for key, value in kwargs.items():
        setattr(calificacion, key, value)
    calificacion.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(calificacion)
    return calificacion


def eliminar(id_inscripcion: UUID, id_evaluacion: UUID) -> bool:
    calificacion = obtener_por_id(id_inscripcion, id_evaluacion)
    if not calificacion:
        return False
    db.delete(calificacion)
    db.commit()
    return True
