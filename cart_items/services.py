from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from config.cnx import SessionLocal
from .model import CartItem
from .dto import CartItemCreate, CartItemUpdate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_cart_items():
    """Obtener todos los elementos del carrito"""
    db = None
    try:
        db = SessionLocal()
        cart_items = db.query(CartItem).all()
        logger.info(f"Se obtuvieron {len(cart_items)} elementos del carrito exitosamente")
        return cart_items
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener elementos del carrito: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def get_cart_items_by_user(user_id: int):
    """Obtener todos los elementos del carrito de un usuario específico"""
    db = None
    try:
        if user_id <= 0:
            raise ValueError("ID de usuario inválido")

        db = SessionLocal()
        # Usar joinedload para cargar los productos y usuarios eficientemente
        cart_items = (
            db.query(CartItem)
            .options(joinedload(CartItem.product))  # Cargar productos en una sola consulta
            .options(joinedload(CartItem.user))     # Cargar usuarios en una sola consulta
            .filter(CartItem.user_id == user_id)
            .all()
        )
        
        # Verificar que todos los items tengan sus productos asociados
        valid_items = []
        for item in cart_items:
            if item.product:
                valid_items.append(item)
            else:
                logger.warning(f"Item de carrito {item.id} sin producto asociado, eliminando...")
                db.delete(item)
        
        if len(valid_items) != len(cart_items):
            db.commit()
            logger.info(f"Se eliminaron {len(cart_items) - len(valid_items)} items inválidos del carrito")
        
        logger.info(f"Se obtuvieron {len(valid_items)} elementos válidos del carrito para el usuario {user_id}")
        return valid_items
    except ValueError:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener carrito del usuario {user_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def get_cart_item_by_id(cart_item_id: int):
    """Obtener un elemento del carrito por ID"""
    db = None
    try:
        if cart_item_id <= 0:
            raise ValueError("ID de elemento del carrito inválido")

        db = SessionLocal()
        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

        if not cart_item:
            logger.warning(f"Elemento del carrito {cart_item_id} no encontrado")
            raise ValueError("Elemento del carrito no encontrado")

        logger.info(f"Elemento del carrito {cart_item_id} obtenido exitosamente")
        return cart_item
    except ValueError:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener elemento del carrito {cart_item_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def create_cart_item(cart_item_data: CartItemCreate):
    """Crear un nuevo elemento del carrito"""
    db = None
    try:
        db = SessionLocal()

        # Verificar si ya existe un item del mismo producto para el mismo usuario
        existing_item = (
            db.query(CartItem)
            .options(joinedload(CartItem.product))
            .options(joinedload(CartItem.user))
            .filter(
                CartItem.user_id == cart_item_data.user_id,
                CartItem.product_id == cart_item_data.product_id
            )
            .first()
        )

        if existing_item:
            # Si ya existe, actualizar la cantidad
            existing_item.quantity += cart_item_data.quantity
            db.commit()
            db.refresh(existing_item)
            logger.info(f"Actualizada cantidad del elemento existente: ID {existing_item.id}, Nueva cantidad: {existing_item.quantity}")
            return existing_item
        else:
            # Si no existe, crear nuevo elemento
            cart_item = CartItem(
                user_id=cart_item_data.user_id,
                product_id=cart_item_data.product_id,
                quantity=cart_item_data.quantity,
            )

            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)

            logger.info(f"Elemento del carrito creado exitosamente: ID {cart_item.id}")
            return cart_item

    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al crear elemento del carrito: {str(e)}")
        raise IntegrityError("Error de integridad de datos", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al crear elemento del carrito: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def update_cart_item(cart_item_id: int, update_data: CartItemUpdate):
    """Actualizar campos de un elemento del carrito existente"""
    db = None
    try:
        db = SessionLocal()

        if cart_item_id <= 0:
            raise ValueError("ID de elemento del carrito inválido")

        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

        if not cart_item:
            logger.warning(f"Intento de actualizar elemento del carrito inexistente: {cart_item_id}")
            raise ValueError("Elemento del carrito no encontrado")

        if update_data.quantity is not None:
            cart_item.quantity = update_data.quantity

        db.commit()
        db.refresh(cart_item)

        logger.info(f"Elemento del carrito {cart_item_id} actualizado exitosamente")
        return cart_item

    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al actualizar elemento del carrito {cart_item_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al actualizar elemento del carrito {cart_item_id}: {str(e)}")
        raise Exception("Error interno al actualizar el elemento del carrito")
    finally:
        if db:
            db.close()


def update_cart_item_quantity(cart_item_id: int, increment: bool = True):
    """Incrementar o decrementar la cantidad de un elemento del carrito"""
    db = None
    try:
        db = SessionLocal()

        if cart_item_id <= 0:
            raise ValueError("ID de elemento del carrito inválido")

        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

        if not cart_item:
            logger.warning(f"Intento de actualizar elemento del carrito inexistente: {cart_item_id}")
            raise ValueError("Elemento del carrito no encontrado")

        # Incrementar o decrementar la cantidad
        if increment:
            cart_item.quantity += 1
        else:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                # Si la cantidad llega a 0, eliminamos el item
                db.delete(cart_item)
                db.commit()
                logger.info(f"Elemento del carrito {cart_item_id} eliminado por cantidad 0")
                return None

        db.commit()
        db.refresh(cart_item)

        logger.info(f"Cantidad del elemento {cart_item_id} actualizada a {cart_item.quantity}")
        return cart_item

    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al actualizar cantidad del elemento {cart_item_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def delete_cart_item(cart_item_id: int):
    """Eliminar un elemento del carrito"""
    db = None
    try:
        if cart_item_id <= 0:
            raise ValueError("ID de elemento del carrito inválido")

        db = SessionLocal()
        cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

        if not cart_item:
            logger.warning(f"Intento de eliminar item {cart_item_id} no encontrado")
            return False

        db.delete(cart_item)
        db.commit()

        logger.info(f"Elemento del carrito {cart_item_id} eliminado exitosamente")
        return True
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al eliminar elemento del carrito {cart_item_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def clear_user_cart(user_id: int):
    """Vaciar todo el carrito de un usuario"""
    db = None
    try:
        if user_id <= 0:
            raise ValueError("ID de usuario inválido")

        db = SessionLocal()
        deleted_count = db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()

        logger.info(f"Carrito del usuario {user_id} vaciado exitosamente. {deleted_count} elementos eliminados")
        return deleted_count
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al vaciar carrito del usuario {user_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()