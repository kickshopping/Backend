from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import ProductCreate, ProductOut, ProductUpdate
from .services import get_all_products, get_product_by_id, create_product, update_product, delete_product

products = APIRouter()

@products.get('', response_model=List[ProductOut], status_code=status.HTTP_200_OK)
def get_products():
    """Obtener todos los productos"""
    try:
        return get_all_products()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener los productos"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener los productos"
        )

@products.get('/{product_id}', response_model=ProductOut, status_code=status.HTTP_200_OK)
def get_product(product_id: int):
    """Obtener un producto por ID"""
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del producto debe ser un numero positivo"
            )
        
        product = get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        return product
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener el producto"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener el producto"
        )

@products.post('', response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def post_product(product: ProductCreate):
    """Crear un nuevo producto"""
    try:
        if not product.name or product.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Datos inválidos: nombre requerido, precio > 0"
            )
        
        return create_product(product)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error de integridad de datos al crear el producto"
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al crear el producto"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al crear el producto"
        )

@products.patch('/{product_id}', response_model=ProductOut, status_code=status.HTTP_200_OK)
def patch_product(product_id: int, update_data: ProductUpdate):
    """Actualizar campos de un producto existente"""
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de producto debe ser un numero positivo"
            )
    
        return update_product(product_id, update_data)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al actualizar el producto"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar el producto"
        )
    
@products.delete('/{product_id}', status_code=status.HTTP_200_OK)
def delete_product_route(product_id: int):
    """Eliminar un producto por ID"""
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de producto debe ser un numero positivo"
            )
        
        eliminado = delete_product(product_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        return {"detail": f"Producto con ID {product_id} eliminado exitosamente"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al eliminar el producto"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al eliminar el producto"
        )
    