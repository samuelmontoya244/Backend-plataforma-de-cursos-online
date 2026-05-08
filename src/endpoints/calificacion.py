from typing import List
from uuid import UUID
from .deps import DbSession, get_current_user_id
from fastapi import APIRouter, HTTPException, status, Depends

from src.services import calificacion as services_calificacion
from src.schemas.response_schema import RespuestaAPI
from src.schemas.calificacion_schema import (
    CalificacionCreate,
    CalificacionUpdate,
    CalificacionResponse,
)

router = APIRouter(prefix="/Calificaciones", tags=["Calificaciones"])


@router.get("", response_model=List[CalificacionResponse])
def listar_calificaciones(db: DbSession, skip: int = 0, limit: int = 100):
    calificacion = services_calificacion.obtener_todos(db, skip=skip, limit=limit)
    return calificacion


@router.get("/{id_inscripcion}/{id_evaluacion}", response_model=CalificacionResponse)
def obtener_calificacion(
    id_inscripcion: UUID, id_evaluacion: UUID, db: DbSession
) -> CalificacionResponse:
    db_calificacion = services_calificacion.obtener_por_id(
        db, id_inscripcion, id_evaluacion
    )
    if not db_calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La calificación no existe en la base de datos",
        )
    return db_calificacion


@router.post(
    "", response_model=CalificacionResponse, status_code=status.HTTP_201_CREATED
)
def crear_calificacion(
    db: DbSession, dato: CalificacionCreate, user_id: str = Depends(get_current_user_id)
):

    try:
        calificacion = services_calificacion.crear(
            db,
            id_usuario_creacion=user_id,
            id_inscripcion=dato.id_inscripcion,
            id_evaluacion=dato.id_evaluacion,
            Nota=dato.Nota,
        )

        return calificacion

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_inscripcion}/{id_evaluacion}", response_model=CalificacionResponse)
def actualizar_calificacion(
    db: DbSession,
    id_inscripcion: UUID,
    id_evaluacion: UUID,
    dato: CalificacionUpdate,
    user_id: str = Depends(get_current_user_id),
):

    calificacion = services_calificacion.actualizar(
        db,
        id_inscripcion=id_inscripcion,
        id_evaluacion=id_evaluacion,
        id_usuario_edita=user_id,
        **dato.model_dump(exclude_unset=True),
    )

    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Calificación no encontrada"
        )

    return calificacion


@router.delete("/{id_inscripcion}/{id_evaluacion}", response_model=RespuestaAPI)
def eliminar_calificacion(
    db: DbSession,
    id_inscripcion: UUID,
    id_evaluacion: UUID,
    user_id: str = Depends(get_current_user_id),
) -> None:
    try:
        # Verificar que la calificación existe
        calificacion_existente = services_calificacion.obtener_por_id(
            db, id_inscripcion, id_evaluacion
        )
        if not calificacion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calificación no encontrada",
            )

        eliminado = services_calificacion.eliminar(
            db, id_inscripcion=id_inscripcion, id_evaluacion=id_evaluacion
        )
        if eliminado:
            return RespuestaAPI(
                mensaje="Calificación eliminada exitosamente", exito=True
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar calificación",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar calificación: {str(e)}",
        )
