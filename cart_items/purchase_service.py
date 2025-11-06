from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from config.cnx import SessionLocal
from .model import CartItem
from datetime import datetime
from usuarios.model import Usuario
import uuid
from .email import send_purchase_ticket_email

def generate_purchase_ticket(user_id: int):
    """
    Genera un ticket de compra a partir de los items en el carrito del usuario.
    """
    db = None
    try:
        db = SessionLocal()
        
        # Obtener los items del carrito con sus productos y usuario
        cart_items = (
            db.query(CartItem)
            .options(joinedload(CartItem.product))
            .options(joinedload(CartItem.user))
            .filter(CartItem.user_id == user_id)
            .all()
        )
        
        if not cart_items:
            raise ValueError("No hay items en el carrito")
            
        # Obtener información del usuario
        user = db.query(Usuario).filter(Usuario.usu_id == user_id).first()
        if not user:
            raise ValueError("Usuario no encontrado")
            
        # Calcular totales y crear items del ticket
        ticket_items = []
        total_amount = 0.0
        
        for item in cart_items:
            if not item.product:
                continue

            # Usar los campos del modelo Product (name, price)
            unit_price = getattr(item.product, 'price', None) or getattr(item.product, 'precio', 0.0)
            product_name = getattr(item.product, 'name', None) or getattr(item.product, 'nombre', 'Producto')
            item_total = (item.quantity or 0) * (unit_price or 0.0)
            ticket_items.append({
                "product_name": product_name,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "total": item_total
            })
            total_amount += item_total
            
        # Generar el ticket
        ticket = {
            "ticket_id": str(uuid.uuid4()),
            # serializar fecha a ISO para que el frontend la entienda sin problemas
            "purchase_date": datetime.now().isoformat(),
            "items": ticket_items,
            "total_amount": total_amount,
            "user_id": getattr(user, 'usu_id', None) or getattr(user, 'user_id', None),
            "user_name": getattr(user, 'usu_nombre_completo', None) or getattr(user, 'usu_usuario', None)
        }
        
        # Limpiar el carrito después de generar el ticket
        for item in cart_items:
            db.delete(item)
        
        db.commit()
        # Intentar enviar el ticket por email a los destinatarios configurados.
        try:
            send_purchase_ticket_email(ticket)
        except Exception:
            # No propagamos error de email al usuario final; ya hemos generado el ticket.
            pass

        return ticket
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        raise SQLAlchemyError(f"Error al generar el ticket: {str(e)}")
    finally:
        if db:
            db.close()