from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.Pago import Pago
from src.services import inscripcion as services_inscripcion
from src.entities.inscripcion import EstadoInscripcion
from src.services import usuario as usuario_services
from src.services import curso as curso_services




def crear(
    db: Session,
    id_usuario: UUID,
    id_usuario_creacion: UUID,
    id_curso: UUID,
    monto: float = None,
    estado_pago: str = None,
    metodo_pago: str = None
) -> Pago:
    
    usuario = usuario_services.obtener_por_id(db, id_usuario)
    if not usuario:
        raise ValueError("El usuario no existe")

    curso = curso_services.obtener_por_id(db, id_curso) 
    if not curso:
        raise ValueError("El curso no existe")

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
    

    if estado_pago == "COMPLETADO":
        inscripcion = services_inscripcion.obtener_por_usuario_y_curso(
            id_usuario, id_curso
        )

        if inscripcion:
            services_inscripcion.actualizar(
                id_inscripcion=inscripcion.id_inscripcion,
                id_usuario_edita=id_usuario_creacion,
                estado_inscripcion=EstadoInscripcion.ACTIVA.value,
            )

    return pago

def obtener_por_id(db: Session, id_pago: UUID) -> Optional[Pago]:
    return (db.query(Pago).filter(Pago.id_pago == id_pago).first())


def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Pago]:
    return db.query(Pago).offset(skip).limit(limit).all()


def obtener_por_usuario(db: Session, id_usuario: UUID) -> List[Pago]:
    return (db.query(Pago).filter(Pago.id_usuario == id_usuario).all())


def actualizar(
    db: Session,
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


def eliminar(db, id_pago: UUID) -> bool:
    pago = obtener_por_id(id_pago)
    if not pago:
        return False
    db.delete(pago)
    db.commit()
    return True
