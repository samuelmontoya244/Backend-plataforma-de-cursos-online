from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from src.entities.Curso import Curso
from src.services import categoria as categoria_services

def crear(
    db: Session,
    id_categoria: UUID,
    nombre_curso: str,
    duracion_horas: int,
    estado_curso: str,
    id_usuario_creacion: UUID,
    descripcion_curso: str | None = None,
) -> Curso:
    curso_existente = db.query(Curso).filter(Curso.nombre_curso == nombre_curso.strip()).first()
    if curso_existente:
        raise ValueError("El curso ya existe")
    
    categoria = categoria_services.obtener_por_id(db, id_categoria)
    if not categoria:
        raise ValueError("La categoría no existe")
    
    curso = Curso(
        id_categoria=id_categoria,
        nombre_curso=nombre_curso.strip(),
        descripcion_curso=descripcion_curso.strip(),
        duracion_horas=duracion_horas,
        estado_curso=estado_curso.strip(),
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso


def obtener_por_id(db: Session, id_curso: UUID) -> Optional[Curso]:
    return db.query(Curso).filter(Curso.id_curso == id_curso).first()


def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Curso]:
    return db.query(Curso).offset(skip).limit(limit).all()


def obtener_por_usuario(db: Session, id_usuario: UUID) -> List[Curso]:
    return db.query(Curso).filter(Curso.id_usuario_creacion == id_usuario).all()


def actualizar(
    db: Session,
    id_curso: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Curso]:
    curso = obtener_por_id(db, id_curso)
    if not curso:
        return None
    for key, value in kwargs.items():
        if hasattr(curso, key):
            setattr(curso, key, value)
    curso.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(curso)
    return curso


def eliminar(db: Session, id_curso: UUID) -> bool:
    curso = obtener_por_id(db, id_curso)
    if not curso:
        return False
    db.delete(curso)
    db.commit()
    return True