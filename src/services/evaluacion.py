from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.evaluacion import Evaluacion

db = SessionLocal()


def crear(
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


def obtener_por_id(id_evaluacion: UUID) -> Optional[Evaluacion]:
    return (
        db.query(Evaluacion).filter(Evaluacion.id_evaluacion == id_evaluacion).first()
    )


def obtener_todos() -> List[Evaluacion]:
    return db.query(Evaluacion).all()


def obtener_por_usuario(id_usuario: UUID) -> List[Evaluacion]:
    return db.query(Evaluacion).filter(Evaluacion.id_usuario == id_usuario).all()


def actualizar(
    id_evaluacion: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Evaluacion]:
    evaluacion = obtener_por_id(id_evaluacion)
    if not evaluacion:
        return None
    for key, value in kwargs.items():
        if hasattr(evaluacion, key):
            setattr(evaluacion, key, value)
    evaluacion.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(evaluacion)
    return evaluacion


def eliminar(id_evaluacion: UUID) -> bool:
    evaluacion = obtener_por_id(id_evaluacion)
    if not evaluacion:
        return False
    db.delete(evaluacion)
    db.commit()
    return True
