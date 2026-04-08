from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.Evaluacion import Evaluacion


def crear(
    db: Session,
    id_leccion: UUID,
    id_usuario_creacion: UUID,
    nombre_evaluacion: str,
    porcentaje: float,
) -> Evaluacion:
    evaluacion = Evaluacion(
        id_leccion=id_leccion,
        id_usuario_creacion=id_usuario_creacion,
        nombre_evaluacion=nombre_evaluacion,
        porcentaje=porcentaje,
    )
    db.add(evaluacion)
    db.commit()
    db.refresh(evaluacion)
    return evaluacion


def obtener_por_id(db: Session, id_evaluacion: UUID) -> Optional[Evaluacion]:
    return (
        db.query(Evaluacion).filter(Evaluacion.id_evaluacion == id_evaluacion).first()
    )
def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Evaluacion]:
    return db.query(Evaluacion).offset(skip).limit(limit).all()


def obtener_por_usuario(db: Session, id_usuario: UUID) -> List[Evaluacion]:
    return db.query(Evaluacion).filter(Evaluacion.id_usuario == id_usuario).all()


def actualizar(
    db: Session,
    id_evaluacion: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Evaluacion]:
    evaluacion = obtener_por_id(db, id_evaluacion)
    if not evaluacion:
        return None
    for key, value in kwargs.items():
        if hasattr(evaluacion, key):
            setattr(evaluacion, key, value)
    evaluacion.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(evaluacion)
    return evaluacion


def eliminar(db: Session, id_evaluacion: UUID) -> bool:
    evaluacion = obtener_por_id(db, id_evaluacion)
    if not evaluacion:
        return False
    db.delete(evaluacion)
    db.commit()
    return True
