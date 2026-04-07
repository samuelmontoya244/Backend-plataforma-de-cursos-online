from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import inscripcion as services_inscripcion
from src.schemas.response_schema import RespuestaAPI
from src.schemas.inscripcion_schema import (
    InscripcionCreate,
    InscripcionUpdate,
    InscripcionResponse,
)

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])

@router.get("", response_model=List[InscripcionResponse])
def listar_inscripciones(db: DbSession, skip: int = 0, limit: int = 100):
    inscripciones = services_inscripcion.obtener_todos(db, skip, limit)
    return inscripciones

@router.get("/{id_inscripcion}", response_model=InscripcionResponse)
def obtener_inscripcion(db: DbSession, id_inscripcion: UUID) -> InscripcionResponse:
    db_inscripcion = services_inscripcion.obtener_por_id(db, id_inscripcion)
    if not db_inscripcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"La inscripción con ID {id_inscripcion} no existe en la base de datos"
        )
    return db_inscripcion

@router.post("", response_model=InscripcionResponse, status_code=status.HTTP_201_CREATED)
def crear_inscripcion(db: DbSession, dato: InscripcionCreate):

    try:
        inscripcion = services_inscripcion.crear(
            db,
            id_curso=dato.id_curso,
            id_usuario_inscrito=dato.id_usuario_inscrito,
            estado_inscripcion=dato.estado_inscripcion,
        )
        return inscripcion

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{id_inscripcion}", response_model=InscripcionResponse)
def actualizar_inscripcion(db: DbSession, id_inscripcion: UUID, dato: InscripcionUpdate):

    inscripcion = services_inscripcion.actualizar(
        db,
        id_inscripcion,
        **dato.model_dump(exclude_unset=True)
    )

    if not inscripcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscripción no encontrada"
        )

    return inscripcion

@router.delete("/{id_inscripcion}", response_model=RespuestaAPI)
def eliminar_inscripcion(db: DbSession, id_inscripcion: UUID) -> None:
    try:
        # Verificar que el usuario existe
        inscripcion_existente = services_inscripcion.obtener_por_id(db, id_inscripcion)
        if not inscripcion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Inscripción no encontrada"
            )

        eliminado = services_inscripcion.eliminar(db, id_inscripcion)
        if eliminado:
            return RespuestaAPI(mensaje="Inscripción eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar inscripción",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar inscripción: {str(e)}",
        )
