from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.certificado import Certificado


def crear(
    db: Session,
    id_inscripcion: UUID,
    id_usuario_creacion: UUID
) -> Certificado:
    certificado = Certificado(
        id_inscripcion=id_inscripcion,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(certificado)
    db.commit()
    db.refresh(certificado)
    return certificado


def obtener_por_id(db: Session, id_certificado: UUID) -> Optional[Certificado]:
    return (
        db.query(Certificado)
        .filter(Certificado.id_certificado == id_certificado)
        .first()
    )


def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Certificado]:
    return db.query(Certificado).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_certificado: UUID,
    id_usuario_edita: UUID = None,
    **kwargs: dict
) -> Optional[Certificado]:
    certificado = obtener_por_id(db, id_certificado)
    if not certificado:
        return None
    for key, value in kwargs.items():
        setattr(certificado, key, value)
    if id_usuario_edita:
        certificado.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(certificado)
    return certificado


def eliminar(db: Session, id_certificado: UUID) -> bool:
    certificado = obtener_por_id(db, id_certificado)
    if not certificado:
        return False
    db.delete(certificado)
    db.commit()
    return True
