from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.curso import Curso

db = SessionLocal()

def crear(
    id_categoria: UUID,
    nombre_curso: str, 
    descripcion_curso: str,
    duracion_horas: int,
    estado_curso: str,
    id_usuario_creacion: UUID) -> Curso:
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

def obtener_por_id(id_curso: UUID) -> Optional[Curso]:
    return db.query(Curso).filter(Curso.id_curso == id_curso).first()

def obtener_todos() -> List[Curso]:
    return db.query(Curso).all()

def obtener_por_usuario(id_usuario: UUID) -> List[Curso]:
    return db.query(Curso).filter(Curso.id_usuario_creacion == id_usuario).all()

def actualizar(
    id_curso: UUID,
    id_usuario_edita: UUID,

    **kwargs: dict,
) -> Optional[Curso]:
    curso = obtener_por_id(id_curso)
    if not curso:
        return None
    for key, value in kwargs.items():
        if hasattr(curso, key):
            setattr(curso, key, value)
    curso.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(curso)
    return curso

def eliminar(id_curso: UUID) -> bool:
    curso = obtener_por_id(id_curso)
    if not curso:
        return False
    db.delete(curso)
    db.commit()
    return True