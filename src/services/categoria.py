from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.categoria import Categoria

db = SessionLocal()


def crear(
    nombre_categoria: str,
    id_usuario_creacion: UUID,
) -> Categoria:
    existente = (
        db.query(Categoria)
        .filter(Categoria.nombre_categoria == nombre_categoria.strip())
        .first()
    )
    if existente:
        raise ValueError("La categoría ya existe")

    categoria = Categoria(
        nombre_categoria=nombre_categoria.strip(),
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def obtener_por_id(id_categoria: UUID) -> Optional[Categoria]:
    return db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()


def obtener_todos() -> List[Categoria]:
    return db.query(Categoria).all()


def actualizar(
    id_categoria: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict
) -> Optional[Categoria]:
    categoria = obtener_por_id(id_categoria)
    if not categoria:
        return None
    for key, value in kwargs.items():
        if hasattr(categoria, key):
            setattr(categoria, key, value)
    categoria.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(categoria)
    return categoria


def eliminar(id_categoria: UUID) -> bool:
    categoria = obtener_por_id(id_categoria)
    if not categoria:
        return False
    db.delete(categoria)
    db.commit()
    return True
