from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import CartItemCreate, CartItemOut, CartItemUpdate, CartItemOutDetailed
from .purchase import PurchaseTicket
from .purchase_service import generate_purchase_ticket
import logging
from middlewares.cart_auth import verify_token_and_permissions

logger = logging.getLogger(__name__)
from .services import (
    get_all_cart_items,
    get_cart_items_by_user,
    get_cart_item_by_id,
    create_cart_item,
    update_cart_item,
    update_cart_item_quantity,
    delete_cart_item,
    clear_user_cart
)

cart_items = APIRouter()



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
                    'image_url': getattr(item.product, 'image_url', None),
                    'description': getattr(item.product, 'description', None),
                    'discount': getattr(item.product, 'discount', 0.0)
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
        # Log the incoming request
        logger.info(f"Recibida solicitud para agregar al carrito: {cart_item.dict()}")
        
        if cart_item.user_id <= 0 or cart_item.product_id <= 0 or cart_item.quantity <= 0:
            logger.warning(f"Datos inválidos en la solicitud: {cart_item.dict()}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Datos inválidos: user_id, product_id y quantity deben ser mayores a 0"
            )
        
        result = create_cart_item(cart_item)
        logger.info(f"Elemento agregado exitosamente al carrito: {result.__dict__}")
        return result
    except HTTPException as he:
        logger.error(f"Error HTTP al crear elemento del carrito: {str(he)}")
        raise
    except ValueError as e:
        logger.error(f"Error de validación al crear elemento del carrito: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError as ie:
        logger.error(f"Error de integridad al crear elemento del carrito: {str(ie)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error de integridad: usuario o producto no válido. Detalles: {str(ie)}"
        )
    except SQLAlchemyError as se:
        logger.error(f"Error de SQLAlchemy al crear elemento del carrito: {str(se)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor al crear el elemento del carrito: {str(se)}"
        )
    except Exception as e:
        logger.error(f"Error inesperado al crear elemento del carrito: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al crear el elemento del carrito: {str(e)}"
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
        
        cart_item = update_cart_item(cart_item_id, update_data)
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
            detail="Error interno del servidor al actualizar el elemento del carrito"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar el elemento del carrito"
        )

@cart_items.post('/{cart_item_id}/increment', response_model=CartItemOut, status_code=status.HTTP_200_OK)
def increment_quantity(cart_item_id: int):
    """Incrementar la cantidad de un elemento del carrito en 1"""
    try:
        if cart_item_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del elemento del carrito debe ser un numero positivo"
            )
        
        cart_item = update_cart_item_quantity(cart_item_id, increment=True)
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
            detail="Error interno del servidor al incrementar la cantidad"
        )

@cart_items.post('/{cart_item_id}/decrement', response_model=CartItemOut, status_code=status.HTTP_200_OK)
def decrement_quantity(cart_item_id: int):
    """Decrementar la cantidad de un elemento del carrito en 1"""
    try:
        if cart_item_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del elemento del carrito debe ser un numero positivo"
            )
        
        cart_item = update_cart_item_quantity(cart_item_id, increment=False)
        if cart_item is None:
            return {"detail": f"Elemento del carrito con ID {cart_item_id} eliminado por cantidad 0"}
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
            detail="Error interno del servidor al decrementar la cantidad"
        )
@cart_items.delete('/{cart_item_id}', status_code=status.HTTP_200_OK)
def delete_cart_item_route(cart_item_id: int, request: Request):
    """Eliminar un elemento del carrito por ID (verifica propiedad y permisos via AuthMiddleware)"""
    try:
        if cart_item_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del elemento del carrito debe ser un numero positivo"
            )

        # AuthMiddleware debe haber colocado el payload JWT en request.state.user
        user_payload = getattr(request.state, 'user', None)
        if not user_payload or 'user_id' not in user_payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autorización requerido")

        # Verificar existencia y propiedad del item
        cart_item = get_cart_item_by_id(cart_item_id)
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Elemento del carrito no encontrado")

        if cart_item.user_id != user_payload['user_id']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para eliminar items de otros usuarios")

        eliminado = delete_cart_item(cart_item_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Elemento del carrito no encontrado"
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


@cart_items.post('/purchase', response_model=PurchaseTicket, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_token_and_permissions)])
def purchase_cart(request: Request):
    """Finalizar la compra y generar ticket (requiere sólo estar autenticado)"""
    try:
        # verify_token_and_permissions dependency ensures token validity and
        # places the payload in request.state.user when appropriate. Use that.
        user_payload = getattr(request.state, 'user', None)
        if not user_payload or 'user_id' not in user_payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autorización requerido")

        user_id = user_payload['user_id']
        return generate_purchase_ticket(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar la compra: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al procesar la compra: {str(e)}"
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