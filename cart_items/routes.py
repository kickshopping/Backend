from fastapi import APIRouter, HTTPException, status
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import CartItemCreate, CartItemOut, CartItemUpdate, CartItemOutDetailed
from .services import (
    get_all_cart_items,
    get_cart_items_by_user,
    get_cart_item_by_id,
    create_cart_item,
    update_cart_item,
    delete_cart_item,
    clear_user_cart
)

cart_items = APIRouter()


@cart_items.delete('/user/{user_id}/clear', status_code=status.HTTP_200_OK)
def clear_cart_for_user(user_id: int):
    """Eliminar todos los elementos del carrito de un usuario"""
    try:
        items = get_cart_items_by_user(user_id)
        for item in items:
            delete_cart_item(item.id)
        return {"detail": f"Carrito del usuario {user_id} vaciado"}
    except Exception as e:
        return {"detail": f"Error al vaciar el carrito: {str(e)}"}


@cart_items.get('', response_model=List[CartItemOut], status_code=status.HTTP_200_OK)
def get_cart_items():
    """Obtener todos los elementos del carrito"""
    try:
        return get_all_cart_items()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener los elementos del carrito"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener los elementos del carrito"
        )


@cart_items.get('/user/{user_id}', response_model=List[CartItemOutDetailed], status_code=status.HTTP_200_OK)
def get_user_cart(user_id: int):
    """Obtener todos los elementos del carrito de un usuario específico"""
    try:
        if user_id <= 0:
            return []
        cart_items_list = get_cart_items_by_user(user_id)
        result = []
        for item in cart_items_list:
            user = None
            if hasattr(item, 'user') and item.user:
                user = {
                    'usu_id': getattr(item.user, 'usu_id', None),
                    'usu_usuario': getattr(item.user, 'usu_usuario', None),
                    'usu_nombre_completo': getattr(item.user, 'usu_nombre_completo', None)
                }
            product = None
            if hasattr(item, 'product') and item.product:
                product = {
                    'id': getattr(item.product, 'id', None),
                    'name': getattr(item.product, 'name', None),
                    'price': getattr(item.product, 'price', None),
                    'image_url': getattr(item.product, 'image_url', None)
                }
            result.append({
                'id': item.id,
                'user_id': item.user_id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'user': user,
                'product': product
            })
        return result
    except Exception:
        # Si hay cualquier error, devolver array vacío
        return []


@cart_items.get('/{cart_item_id}', response_model=CartItemOut, status_code=status.HTTP_200_OK)
def get_cart_item(cart_item_id: int):
    """Obtener un elemento del carrito por ID"""
    try:
        if cart_item_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del elemento del carrito debe ser un numero positivo"
            )
        
        cart_item = get_cart_item_by_id(cart_item_id)
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Elemento del carrito con ID {cart_item_id} no encontrado"
            )
        return cart_item
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
            detail="Error interno del servidor al obtener el elemento del carrito"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener el elemento del carrito"
        )


@cart_items.post('', response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
def post_cart_item(cart_item: CartItemCreate):
    """Crear un nuevo elemento del carrito o actualizar si ya existe"""
    try:
        if cart_item.user_id <= 0 or cart_item.product_id <= 0 or cart_item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Datos inválidos: user_id, product_id y quantity deben ser mayores a 0"
            )
        
        return create_cart_item(cart_item)
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
            detail="Error de integridad: usuario o producto no válido"
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al crear el elemento del carrito"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al crear el elemento del carrito"
        )


@cart_items.patch('/{cart_item_id}', response_model=CartItemOut, status_code=status.HTTP_200_OK)
def patch_cart_item(cart_item_id: int, update_data: CartItemUpdate):
    """Actualizar campos de un elemento del carrito existente"""
    try:
        if cart_item_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del elemento del carrito debe ser un numero positivo"
            )
    
        return update_cart_item(cart_item_id, update_data)
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
            detail="Error interno del servidor al actualizar el elemento del carrito"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar el elemento del carrito"
        )


@cart_items.delete('/{cart_item_id}', status_code=status.HTTP_200_OK)
def delete_cart_item_route(cart_item_id: int):
    """Eliminar un elemento del carrito por ID"""
    try:
        if cart_item_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del elemento del carrito debe ser un numero positivo"
            )
        
        eliminado = delete_cart_item(cart_item_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Elemento del carrito con ID {cart_item_id} no encontrado"
            )
        return {"detail": f"Elemento del carrito con ID {cart_item_id} eliminado exitosamente"}
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
            detail="Error interno del servidor al eliminar el elemento del carrito"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al eliminar el elemento del carrito"
        )


@cart_items.delete('/user/{user_id}/clear', status_code=status.HTTP_200_OK)
def clear_cart(user_id: int):
    """Vaciar todo el carrito de un usuario"""
    try:
        if user_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del usuario debe ser un numero positivo"
            )
        
        deleted_count = clear_user_cart(user_id)
        return {
            "detail": f"Carrito del usuario {user_id} vaciado exitosamente",
            "items_removed": deleted_count
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al vaciar el carrito"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al vaciar el carrito"
        )