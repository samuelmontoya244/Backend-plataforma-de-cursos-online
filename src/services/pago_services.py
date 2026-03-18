from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.Pago import Pago

db = SessionLocal()


def crear(
    id_usuario: UUID,
    id_usuario_creacion: UUID,
    id_curso: UUID,
    monto: float,
    estado_pago: str,
    metodo_pago: str,
) -> Pago:
    pago = Pago(
        id_usuario=id_usuario,
        id_usuario_creacion=id_usuario_creacion,
        id_curso=id_curso,
        monto=monto,
        estado_pago=estado_pago,
        metodo_pago=metodo_pago,
    )
    db.add(pago)
    db.commit()
    db.refresh(pago)
    return pago


def obtener_por_id(id_pago: UUID) -> Optional[Pago]:
    return db.query(Pago).filter(Pago.id_pago == id_pago).first()


def obtener_todos() -> List[Pago]:
    return db.query(Pago).all()


def obtener_por_usuario(id_usuario: UUID) -> List[Pago]:
    return db.query(Pago).filter(Pago.id_usuario == id_usuario).all()


def actualizar(
    id_pago: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Pago]:
    pago = obtener_por_id(id_pago)
    if not pago:
        return None
    for key, value in kwargs.items():
        if hasattr(pago, key):
            setattr(pago, key, value)
    pago.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(pago)
    return pago


def eliminar(id_pago: UUID) -> bool:
    pago = obtener_por_id(id_pago)
    if not pago:
        return False
    db.delete(pago)
    db.commit()
    return True
