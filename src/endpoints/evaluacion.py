from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from .deps import DbSession, get_current_user_id

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
             status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La evlauacion con ID {id_evaluacion} no existe en la base de datos",
        )
    return db_evaluacion        


@router.post("", response_model=EvaluacionResponse, status_code=status.HTTP_201_CREATED)
def crear_evaluacion(db: DbSession, dato: EvaluacionCreate,user_id: str = Depends(get_current_user_id)):
    try:
        evaluacion = services_evaluacion.crear(
            db,
            id_leccion=dato.id_leccion,
            nombre_evaluacion=dato.nombre_evaluacion,
            porcentaje=dato.porcentaje,
            id_usuario_creacion=user_id,
        )
        return evaluacion
    except ValueError as e:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_evaluacion}", response_model=EvaluacionResponse)
def actualizar_evaluacion(db: DbSession, id_evaluacion: UUID, dato: EvaluacionUpdate, user_id: str = Depends(get_current_user_id)):
    evaluacion = services_evaluacion.actualizar(
        db, id_evaluacion, id_usuario_edita=user_id, **dato.model_dump(exclude_unset=True)
    )

    if not evaluacion:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Evaluación no encontrada"
        )

    return evaluacion


@router.delete("/{id_evaluacion}", response_model=RespuestaAPI)
def eliminar_evaluacion(db: DbSession, id_evaluacion: UUID,user_id: str = Depends(get_current_user_id)) -> None:
    try:
        evaluacion_existente = services_evaluacion.obtener_por_id(db, id_evaluacion)
        if not evaluacion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Evaluación no encontrada"
            )
        
        if evaluacion_existente.id_usuario_creacion != UUID(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No autorizado para eliminar esta evaluación"
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