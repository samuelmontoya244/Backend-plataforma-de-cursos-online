from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import evaluacion as services_evaluacion
from src.schemas.response_schema import RespuestaAPI
from src.schemas.evaluacion_schema import (
    EvaluacionCreate,
    EvaluacionUpdate,
    EvaluacionResponse,
)

router = APIRouter(prefix="/evaluaciones", tags=["evaluaciones"])


@router.get("", response_model=List[EvaluacionResponse])
def listar_evaluaciones(db: DbSession, skip: int = 0, limit: int = 100):
    evaluaciones = services_evaluacion.obtener_todos(db, skip, limit)
    return evaluaciones


@router.get("/{id_evaluacion}", response_model=EvaluacionResponse)
def obtener_evaluacion(db: DbSession, id_evaluacion: UUID) -> EvaluacionResponse:
    db_evaluacion = services_evaluacion.obtener_por_id(db, id_evaluacion)
    if not db_evaluacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"La evaluación con ID {id_evaluacion} no existe en la base de datos"
        )
    return db_evaluacion


@router.post("", response_model=EvaluacionResponse, status_code=status.HTTP_201_CREATED)
def crear_evaluacion(db: DbSession, dato: EvaluacionCreate):
    try:
        evaluacion = services_evaluacion.crear(
            db,
            id_leccion=dato.id_leccion,
            nombre_evaluacion=dato.nombre_evaluacion,
            porcentaje=dato.porcentaje,
            id_usuario_creacion=dato.id_usuario_creacion,
        )
        return evaluacion
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_evaluacion}", response_model=EvaluacionResponse)
def actualizar_evaluacion(db: DbSession, id_evaluacion: UUID, dato: EvaluacionUpdate):
    evaluacion = services_evaluacion.actualizar(
        db,
        id_evaluacion,
        **dato.model_dump(exclude_unset=True)
    )

    if not evaluacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluación no encontrada"
        )

    return evaluacion


@router.delete("/{id_evaluacion}", response_model=RespuestaAPI)
def eliminar_evaluacion(db: DbSession, id_evaluacion: UUID) -> None:
    try:
        evaluacion_existente = services_evaluacion.obtener_por_id(db, id_evaluacion)
        if not evaluacion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Evaluación no encontrada"
            )

        eliminado = services_evaluacion.eliminar(db, id_evaluacion)
        if eliminado:
            return RespuestaAPI(mensaje="Evaluación eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar evaluación",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar evaluación: {str(e)}",
        )