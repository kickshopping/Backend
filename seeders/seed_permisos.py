"""
Seeder para la carga inicial de permisos del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from permisos.model import Permiso

def create_permissions_table():
    """Crear las tablas de permisos si no existen"""
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✓ Tablas de permisos creadas correctamente")
    except Exception as e:
        print(f"✗ Error al crear tablas: {e}")

def seed_permisos():
    """Crear permisos básicos del sistema"""
    db = SessionLocal()
    
    try:
        print("=== Iniciando carga de permisos ===")
        
        # Definir permisos basados en las rutas reales existentes
        permisos_base = [
            # === PERMISOS DE USUARIOS ===
            {
                "permiso_nombre": "usuarios.listar",
                "permiso_ruta": "/usuarios",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar usuarios del sistema"
            },
            {
                "permiso_nombre": "usuarios.crear",
                "permiso_ruta": "/usuarios",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Crear nuevos usuarios"
            },
            {
                "permiso_nombre": "usuarios.ver_perfil",
                "permiso_ruta": "/usuarios/me",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver perfil del usuario autenticado"
            },
            {
                "permiso_nombre": "usuarios.ver",
                "permiso_ruta": "/usuarios/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de un usuario"
            },
            {
                "permiso_nombre": "usuarios.actualizar",
                "permiso_ruta": "/usuarios/{id}",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar usuario"
            },
            {
                "permiso_nombre": "usuarios.eliminar",
                "permiso_ruta": "/usuarios/{id}",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Eliminar usuario"
            },
            {
                "permiso_nombre": "usuarios.login",
                "permiso_ruta": "/usuarios/login",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Iniciar sesión"
            },
            
            # === PERMISOS DE ROLES ===
            {
                "permiso_nombre": "roles.listar",
                "permiso_ruta": "/roles",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar roles del sistema"
            },
            {
                "permiso_nombre": "roles.crear",
                "permiso_ruta": "/roles",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Crear nuevos roles"
            },
            {
                "permiso_nombre": "roles.ver",
                "permiso_ruta": "/roles/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de un rol"
            },
            {
                "permiso_nombre": "roles.actualizar",
                "permiso_ruta": "/roles/{id}",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar rol"
            },
            {
                "permiso_nombre": "roles.eliminar",
                "permiso_ruta": "/roles/{id}",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Eliminar rol"
            },
            
            # === PERMISOS DE PRODUCTOS ===
            {
                "permiso_nombre": "productos.listar",
                "permiso_ruta": "/productos",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar productos"
            },
            {
                "permiso_nombre": "productos.crear",
                "permiso_ruta": "/productos",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Crear nuevos productos"
            },
            {
                "permiso_nombre": "productos.ver",
                "permiso_ruta": "/productos/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de un producto"
            },
            {
                "permiso_nombre": "productos.actualizar",
                "permiso_ruta": "/productos/{id}",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar producto"
            },
            {
                "permiso_nombre": "productos.eliminar",
                "permiso_ruta": "/productos/{id}",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Eliminar producto"
            },
            
            # === PERMISOS DE CARRITO ===
            {
                "permiso_nombre": "cart_items.listar",
                "permiso_ruta": "/cart_items",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar elementos del carrito"
            },
            {
                "permiso_nombre": "cart_items.ver_usuario",
                "permiso_ruta": "/cart_items/user/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver carrito de un usuario específico"
            },
            {
                "permiso_nombre": "cart_items.ver",
                "permiso_ruta": "/cart_items/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de un elemento del carrito"
            },
            {
                "permiso_nombre": "cart_items.crear",
                "permiso_ruta": "/cart_items",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Agregar elemento al carrito"
            },
            {
                "permiso_nombre": "cart_items.actualizar",
                "permiso_ruta": "/cart_items/{id}",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar elemento del carrito"
            },
            {
                "permiso_nombre": "cart_items.eliminar",
                "permiso_ruta": "/cart_items/{id}",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Eliminar elemento del carrito"
            },
            {
                "permiso_nombre": "cart_items.limpiar_carrito",
                "permiso_ruta": "/cart_items/user/{id}/clear",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Limpiar carrito de un usuario"
            },
            
            # === PERMISOS DE PERMISOS (META-PERMISOS) ===
            {
                "permiso_nombre": "permisos.listar",
                "permiso_ruta": "/permisos",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Listar permisos del sistema"
            },
            {
                "permiso_nombre": "permisos.crear",
                "permiso_ruta": "/permisos",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Crear nuevos permisos"
            },
            {
                "permiso_nombre": "permisos.ver",
                "permiso_ruta": "/permisos/{id}",
                "permiso_metodo": "GET",
                "permiso_descripcion": "Ver detalles de un permiso"
            },
            {
                "permiso_nombre": "permisos.actualizar",
                "permiso_ruta": "/permisos/{id}",
                "permiso_metodo": "PATCH",
                "permiso_descripcion": "Actualizar permisos"
            },
            {
                "permiso_nombre": "permisos.eliminar",
                "permiso_ruta": "/permisos/{id}",
                "permiso_metodo": "DELETE",
                "permiso_descripcion": "Eliminar permisos"
            },
            {
                "permiso_nombre": "permisos.asignar_rol",
                "permiso_ruta": "/permisos/assign",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Asignar permisos a roles"
            },
            {
                "permiso_nombre": "permisos.remover_rol",
                "permiso_ruta": "/permisos/remove",
                "permiso_metodo": "POST",
                "permiso_descripcion": "Remover permisos de roles"
            }
        ]
        
        permisos_creados = 0
        
        for permiso_data in permisos_base:
            # Verificar si el permiso ya existe
            existing = db.query(Permiso).filter(
                Permiso.permiso_ruta == permiso_data["permiso_ruta"],
                Permiso.permiso_metodo == permiso_data["permiso_metodo"]
            ).first()
            
            if not existing:
                permiso = Permiso(**permiso_data)
                db.add(permiso)
                permisos_creados += 1
                print(f"✓ Creado permiso: {permiso_data['permiso_nombre']}")
            else:
                print(f"- Ya existe permiso: {permiso_data['permiso_nombre']}")
        
        db.commit()
        print(f"\n✓ {permisos_creados} permisos creados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error al crear permisos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Permisos ===")
    create_permissions_table()
    seed_permisos()
    print("=== Finalizado ===")