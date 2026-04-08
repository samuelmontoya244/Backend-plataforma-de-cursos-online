from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

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


@router.get("/{id_calificacion}", response_model=CalificacionResponse)
def obtener_calificacion(id_calificacion: UUID, db: DbSession) -> CalificacionResponse:
    db_calificacion = services_calificacion.obtener_por_id(db, id_calificacion)
    if not db_calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"La calificación con ID {id_calificacion} no existe en la base de datos"
        )
    return db_calificacion


@router.post("", response_model=CalificacionResponse, status_code=status.HTTP_201_CREATED)
def crear_calificacion(db: DbSession, dato: CalificacionCreate):

    try:
        calificacion = services_calificacion.crear(
            db,
            id_usuario_creacion=dato.id_usuario_creacion,
            id_inscripcion=dato.id_inscripcion,
            id_evaluacion=dato.id_evaluacion,
            Nota=dato.Nota
        )
        
        return calificacion

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_calificacion}", response_model=CalificacionResponse)
def actualizar_calificacion(db: DbSession, id_calificacion: UUID, dato: CalificacionUpdate):

    calificacion = services_calificacion.actualizar(
        db,
        id_calificacion,
        **dato.model_dump(exclude_unset=True)
    )

    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificación no encontrada"
        )

    return calificacion


@router.delete("/{id_calificacion}", response_model=RespuestaAPI)
def eliminar_calificacion(db: DbSession, id_calificacion: UUID) -> None:
    try:
        # Verificar que el usuario existe
        usuario_existente = services_calificacion.obtener_por_id(db, id_calificacion)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Calificación no encontrada"
            )

        eliminado = services_calificacion.eliminar(db, id_calificacion=id_calificacion)
        if eliminado:
            return RespuestaAPI(mensaje="Calificación eliminada exitosamente", exito=True)
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