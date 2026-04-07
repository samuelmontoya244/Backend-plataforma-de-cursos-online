from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import curso as services_curso
from src.schemas.curso_schema import (
    CursoCreate,
    CursoUpdate,
    CursoRead,
    CursoResponse,
    RespuestaAPI
)

router = APIRouter(prefix="/cursos", tags=["cursos"])


@router.get("", response_model=List[CursoResponse])
def listar_cursos(db: DbSession):
    cursos = services_curso.obtener_todos()
    return cursos


@router.get("/{id_curso}", response_model=CursoRead)
def obtener_curso(id_curso: UUID, db: DbSession) -> CursoRead:
    db_curso = services_curso.obtener_por_id(id_curso)
    if not db_curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"El curso con ID {id_curso} no existe en la base de datos"
        )
    return db_curso


@router.post("", response_model=CursoRead, status_code=status.HTTP_201_CREATED)
def crear_curso(dato: CursoCreate):

    try:
        curso = services_curso.crear(
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


@router.put("/{id_curso}", response_model=CursoRead)
def actualizar_curso(id_curso: UUID, dato: CursoUpdate, db: DbSession):

    curso = services_curso.actualizar(
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
def eliminar_curso(id_curso: UUID, db: DbSession) -> None:
    try:
        # Verificar que el curso existe
        curso_existente = services_curso.obtener_por_id(id_curso)
        if not curso_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado"
            )

        eliminado = services_curso.eliminar(id_curso)
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
