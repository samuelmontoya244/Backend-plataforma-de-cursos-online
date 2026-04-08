from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from .deps import DbSession

from src.services import categoria as services_categoria
from src.schemas.response_schema import RespuestaAPI
from src.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
)

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("", response_model=List[CategoriaResponse])
def listar_categorias(db: DbSession, skip: int = 0, limit: int = 100):
    categorias = services_categoria.obtener_todos(db, skip, limit)
    return categorias

@router.get("/{id_categoria}", response_model=CategoriaResponse)
def obtener_categoria(db: DbSession, id_categoria: UUID) -> CategoriaResponse:
    db_categoria = services_categoria.obtener_por_id(db, id_categoria)
    if not db_categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"La categoria con ID {id_categoria} no existe en la base de datos"
        )
    return db_categoria

@router.post("", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_categoria(db: DbSession, dato: CategoriaCreate):

    try:
        categoria = services_categoria.crear(
            db,
            nombre_categoria=dato.nombre_categoria,
            id_usuario_creacion=dato.id_usuario_creacion
        )
        return categoria

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{id_categoria}", response_model=CategoriaResponse)
def actualizar_categoria(db: DbSession, id_categoria: UUID, dato: CategoriaUpdate):

    categoria = services_categoria.actualizar(
        db,
        id_categoria,
        **dato.model_dump(exclude_unset=True)
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )

    return categoria

@router.delete("/{id_categoria}", response_model=RespuestaAPI)
def eliminar_categoria(db: DbSession, id_categoria: UUID) -> None:
    try:
        # Verificar que la categoría existe
        categoria_existente = services_categoria.obtener_por_id(db, id_categoria)
        if not categoria_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )

        eliminado = services_categoria.eliminar(db, id_categoria)
        if eliminado:
            return RespuestaAPI(mensaje="Categoría eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar categoría",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar categoría: {str(e)}",
        )