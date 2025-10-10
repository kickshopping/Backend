from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from config.cnx import SessionLocal
from .model import Product
from .dto import ProductCreate, ProductUpdate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_products():
    """Obtener todos los productos"""
    db = None
    try:
        db = SessionLocal()
        products = db.query(Product).all()
        logger.info(f"Se obtuvieron {len(products)} productos exitosamente")
        return products
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener productos: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def get_product_by_id(product_id: int):
    """Obtener un producto por ID"""
    db = None
    try:
        if product_id <= 0:
            raise ValueError("ID de producto inválido")

        db = SessionLocal()
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            logger.warning(f"Producto {product_id} no encontrado")
            raise ValueError("Producto no encontrado")

        logger.info(f"Producto {product_id} obtenido exitosamente")
        return product
    except ValueError:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener producto {product_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def create_product(product_data: ProductCreate):
    """Crear un nuevo producto"""
    db = None
    try:
        db = SessionLocal()

        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            image_url=product_data.image_url,
            discount=product_data.discount,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        logger.info(f"Producto creado exitosamente: ID {product.id}, Nombre: {product.name}")
        return product
    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al crear producto: {str(e)}")
        raise IntegrityError("Error de integridad de datos", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al crear producto: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()


def update_product(product_id: int, update_data: ProductUpdate):
    """Actualizar campos de un producto existente"""
    db = None
    try:
        db = SessionLocal()

        if product_id <= 0:
            raise ValueError("ID de producto inválido")

        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            logger.warning(f"Intento de actualizar producto inexistente: {product_id}")
            raise ValueError("Producto no encontrado")

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)

        logger.info(f"Producto {product_id} actualizado exitosamente")
        return product

    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al actualizar producto {product_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al actualizar producto {product_id}: {str(e)}")
        raise Exception("Error interno al actualizar el producto")
    finally:
        if db:
            db.close()


def delete_product(product_id: int):
    """Eliminar un producto"""
    db = None
    try:
        if product_id <= 0:
            raise ValueError("ID de producto inválido")

        db = SessionLocal()
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise ValueError("Producto no encontrado")

        db.delete(product)
        db.commit()

        logger.info(f"Producto {product_id} eliminado exitosamente")
        return True
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al eliminar producto {product_id}: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    finally:
        if db:
            db.close()
