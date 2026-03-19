from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.certificado import Certificado

db = SessionLocal()


def crear(id_inscripcion: UUID, id_usuario_creacion: UUID) -> Certificado:
    certificado = Certificado(
        id_inscripcion=id_inscripcion,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(certificado)
    db.commit()
    db.refresh(certificado)
    return certificado


def obtener_por_id(id_certificado: UUID) -> Optional[Certificado]:
    return (
        db.query(Certificado)
        .filter(Certificado.id_certificado == id_certificado)
        .first()
    )


def obtener_todos() -> List[Certificado]:
    return db.query(Certificado).all()


def actualizar(
    id_certificado: UUID, id_usuario_edita: UUID, **kwargs: dict
) -> Optional[Certificado]:
    certificado = obtener_por_id(id_certificado)
    if not certificado:
        return None
    for key, value in kwargs.items():
        setattr(certificado, key, value)
    certificado.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(certificado)
    return certificado


def eliminar(id_certificado: UUID) -> bool:
    certificado = obtener_por_id(id_certificado)
    if not certificado:
        return False
    db.delete(certificado)
    db.commit()
    return True
