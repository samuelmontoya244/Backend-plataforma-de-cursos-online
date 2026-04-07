from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import leccion as services_leccion
from src.schemas.leccion_schema import (
    LeccionCreate,
    LeccionUpdate,
    LeccionRead,
    LeccionResponse,
    RespuestaAPI
)

router = APIRouter(prefix="/lecciones", tags=["lecciones"])


@router.get("", response_model=List[LeccionRead])
def listar_lecciones(db: DbSession, skip: int = 0, limit: int = 100) -> List[LeccionRead]:
    return services_leccion.listar(db, skip=skip, limit=limit)



@router.get("/{id_leccion}", response_model=LeccionRead)
def obtener_leccion(id_leccion: UUID, db: DbSession) -> LeccionRead:
    db_leccion = services_leccion.obtener_por_id(id_leccion)
    if not db_leccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"La lección con ID {id_leccion} no existe en la base de datos"
        )
    return db_leccion


@router.post("", response_model=LeccionRead, status_code=status.HTTP_201_CREATED)
def crear_leccion(dato: LeccionCreate):

    try:
        leccion = services_leccion.crear(
            id_usuario_creacion=dato.id_usuario_creacion,
            id_curso=dato.id_curso,
            titulo_leccion=dato.titulo_leccion,
            descripcion_leccion=dato.descripcion_leccion,
            orden=dato.orden,
            duracion_horas=dato.duracion_horas
        )
        return leccion

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_leccion}", response_model=LeccionRead)
def actualizar_leccion(id_leccion: UUID, dato: LeccionUpdate, db: DbSession):

    leccion = services_leccion.actualizar(
        id_leccion,
        **dato.model_dump(exclude_unset=True)
    )

    if not leccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lección no encontrada"
        )

    return leccion


@router.delete("/{id_leccion}", response_model=RespuestaAPI)
def eliminar_leccion(id_leccion: UUID, db: DbSession) -> None:
    try:
        # Verificar que el usuario existe
        usuario_existente = services_leccion.obtener_por_id(id_leccion)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Lección no encontrada"
            )

        eliminado = services_leccion.eliminar(id_leccion=id_leccion)
        if eliminado:
            return RespuestaAPI(mensaje="Lección eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar lección",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar lección: {str(e)}",
        )
