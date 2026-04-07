from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.database.config import SessionLocal
from src.entities.categoria import Categoria


def crear(
    db: Session,
    nombre_categoria: str,
    id_usuario_creacion: UUID,
) -> Categoria:
    categoria_existente = (
        db.query(Categoria)
        .filter(Categoria.nombre_categoria == nombre_categoria.strip())
        .first()
    )
    
    if categoria_existente:
        raise ValueError("La categoría ya existe")

    categoria = Categoria(
        nombre_categoria=nombre_categoria.strip(),
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def obtener_por_id(db, id_categoria: UUID) -> Optional[Categoria]:
    return db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()


def obtener_todos(db, skip: int = 0, limit: int = 100) -> List[Categoria]:
    return db.query(Categoria).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_categoria: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict
) -> Optional[Categoria]:
    categoria = obtener_por_id(db, id_categoria)
    if not categoria:
        return None
    for key, value in kwargs.items():
        if hasattr(categoria, key):
            setattr(categoria, key, value)
    categoria.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(categoria)
    return categoria


def eliminar(db: Session, id_categoria: UUID) -> bool:
    categoria = obtener_por_id(db, id_categoria)
    if not categoria:
        return False
    db.delete(categoria)
    db.commit()
    return True
