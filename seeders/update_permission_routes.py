import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal
from sqlalchemy import text


if __name__ == '__main__':
    db = SessionLocal()
    try:
        # Update cart_items placeholder to {id}
        sql = text("""
            UPDATE permisos
            SET permiso_ruta = REPLACE(permiso_ruta, '{cart_item_id}', '{id}')
            WHERE permiso_ruta LIKE '%{cart_item_id}%'
        """)
        res = db.execute(sql)
        db.commit()
        print(f"Updated {res.rowcount if hasattr(res, 'rowcount') else 'unknown'} permiso_ruta rows replacing '{{cart_item_id}}' -> '{{id}}'")
    except Exception as e:
        db.rollback()
        print('Error updating permiso_ruta:', e)
    finally:
        db.close()
