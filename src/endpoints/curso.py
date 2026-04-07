from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import curso as services_curso
from src.schemas.response_schema import RespuestaAPI
from src.schemas.curso_schema import (
    CursoCreate,
    CursoUpdate,
    CursoResponse,
)

router = APIRouter(prefix="/cursos", tags=["cursos"])

@router.get("", response_model=List[CursoResponse])
def listar_cursos(db: DbSession, skip: int = 0, limit: int = 100):
    cursos = services_curso.obtener_todos(db, skip, limit)
    return cursos

@router.get("/{id_curso}", response_model=CursoResponse)
def obtener_curso(db: DbSession, id_curso: UUID) -> CursoResponse:
    db_curso = services_curso.obtener_por_id(db, id_curso)
    if not db_curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"El curso con ID {id_curso} no existe en la base de datos"
        )
    return db_curso

@router.post("", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def crear_curso(db: DbSession, dato: CursoCreate):

    try:
        curso = services_curso.crear(
            db,
            id_categoria=dato.id_categoria,
            nombre_curso=dato.nombre_curso,
            duracion_horas=dato.duracion_horas,
        )
        return curso

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{id_curso}", response_model=CursoResponse)
def actualizar_curso(db: DbSession, id_curso: UUID, dato: CursoUpdate):

    curso = services_curso.actualizar(
        db,
        id_curso,
        **dato.model_dump(exclude_unset=True)
    )

    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso no encontrado"
        )

    return curso

@router.delete("/{id_curso}", response_model=RespuestaAPI)
def eliminar_curso(db: DbSession, id_curso: UUID) -> None:
    try:
        # Verificar que el curso existe
        curso_existente = services_curso.obtener_por_id(db, id_curso)
        if not curso_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado"
            )

        eliminado = services_curso.eliminar(db, id_curso)
        if eliminado:
            return RespuestaAPI(mensaje="Curso eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar curso",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar curso: {str(e)}",
        )
