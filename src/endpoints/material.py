from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import material as services_material
from src.schemas.response_schema import RespuestaAPI
from src.schemas.material_schema import (
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse,
)

router = APIRouter(prefix="/material", tags=["materiales"])


@router.get("", response_model=List[MaterialResponse])
def listar_materiales(db: DbSession, skip: int = 0, limit: int = 100) -> List[MaterialResponse]:
    return services_material.listar(db, skip=skip, limit=limit)


@router.get("/{id_material}", response_model=MaterialResponse)
def obtener_material(id_material: UUID, db: DbSession) -> MaterialResponse:
    db_material = services_material.obtener_por_id(id_material)
    if not db_material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"El material con ID {id_material} no existe en la base de datos"
        )
    return db_material


@router.post("", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
def crear_material(dato: MaterialCreate):

    try:
        material = services_material.crear(
            id_usuario_creacion=dato.id_usuario_creacion,
            id_leccion=dato.id_leccion,
            titulo_material=dato.titulo_material,
            tipo_material=dato.tipo_material,
            URL_archivo=dato.URL_archivo
        )
        return material

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{id_material}", response_model=MaterialResponse)
def actualizar_material(id_material: UUID, dato: MaterialUpdate, db: DbSession):

    material = services_material.actualizar(
        id_material,
        **dato.model_dump(exclude_unset=True)
    )

    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material no encontrado"
        )

    return material


@router.delete("/{id_material}", response_model=RespuestaAPI)
def eliminar_material(id_material: UUID, db: DbSession) -> None:
    try:
        # Verificar que el usuario existe
        usuario_existente = services_material.obtener_por_id(id_material)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material no encontrado"
            )

        eliminado = services_material.eliminar(id_material=id_material)
        if eliminado:
            return RespuestaAPI(mensaje="Material eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar material",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar material: {str(e)}",
        )