# Eliminar la tabla de usuarios completamente
def drop_usuarios_table():
    from config.cnx import engine
    from .model import Usuario
    Usuario.__table__.drop(engine)
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

from config.cnx import SessionLocal
from .model import Usuario
from .dto import UsuarioCreate, UsuarioUpdate

# Preferir las constantes centrales de config/auth.py para evitar divergencias
from config.auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

load_dotenv()

# Asegurar que ACCESS_TOKEN_EXPIRE_MINUTES y REFRESH_TOKEN_EXPIRE_DAYS sean enteros y razonables
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
except Exception:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

try:
    REFRESH_TOKEN_EXPIRE_DAYS = int(REFRESH_TOKEN_EXPIRE_DAYS)
except Exception:
    REFRESH_TOKEN_EXPIRE_DAYS = 7

# Limitar expiraciones para evitar OverflowError (p.ej. valores mal formados en .env)
MAX_MINUTES = 60 * 24 * 365 * 10  # 10 años en minutos
if ACCESS_TOKEN_EXPIRE_MINUTES <= 0 or ACCESS_TOKEN_EXPIRE_MINUTES > MAX_MINUTES:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
if REFRESH_TOKEN_EXPIRE_DAYS <= 0 or REFRESH_TOKEN_EXPIRE_DAYS > (365*10):
    REFRESH_TOKEN_EXPIRE_DAYS = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    # Usar timezone-aware UTC para consistencia
    now = datetime.now(timezone.utc)
    delta = expires_delta if expires_delta is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Proteger contra valores absurdos
    if delta.total_seconds() > MAX_MINUTES * 60:
        delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = now + delta
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    delta = expires_delta if expires_delta is not None else timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    # Proteger contra valores absurdos
    if delta.total_seconds() > (365*10)*24*3600:
        delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    expire = now + delta
    # mark token type as refresh to differentiate
    to_encode.update({"exp": int(expire.timestamp()), "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Aquí podrías realizar validaciones adicionales si lo necesitas
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


def get_all_usuarios():
    db = None
    try:
        print("Obteniendo todos los usuarios...********************************")
        db = SessionLocal()
        usuarios = db.query(Usuario).all()
        if not usuarios:
            raise ValueError("No hay usuarios registrados")
        return usuarios
    finally:
        if db:
            db.close()


def get_usuario_by_id(usu_id: int):
    db = None
    try:
        db = SessionLocal()
        usuario = db.query(Usuario).filter(Usuario.usu_id == usu_id).first()
        if not usuario:
            raise ValueError(f"Usuario con ID {usu_id} no encontrado")
        # Extraer el nombre del rol antes de cerrar la sesión
        user_dict = usuario.__dict__.copy()
        if usuario.rol:
            user_dict["rol_nombre"] = usuario.rol.rol_nombre
        return user_dict
    finally:
        if db:
            db.close()


def create_usuario(usuario: UsuarioCreate):
    db = None
    try:
        from middlewares.auth import hash_password
        db = SessionLocal()
        
        # Asignar siempre el rol de comprador (rol_id=2)
        nuevo_usuario = Usuario(
            usu_usuario=usuario.usu_usuario,
            usu_contrasenia=hash_password(usuario.usu_contrasenia),
            usu_rol_id=2,
            usu_nombre_completo=usuario.usu_nombre_completo,
            birthdate=usuario.birthdate,
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()


def update_usuario(usu_id: int, update_data: UsuarioUpdate):
    db = None
    try:
        db = SessionLocal()
        usuario = db.query(Usuario).filter(Usuario.usu_id == usu_id).first()
        if not usuario:
            raise ValueError(f"Usuario con ID {usu_id} no encontrado")

        if update_data.usu_nombre_completo:
            usuario.usu_nombre_completo = update_data.usu_nombre_completo # type: ignore
        if update_data.usu_contrasenia:
            usuario.usu_contrasenia = update_data.usu_contrasenia  # type: ignore
        if update_data.usu_rol_id:
            usuario.usu_rol_id = update_data.usu_rol_id # type: ignore
        if update_data.birthdate is not None:
            usuario.birthdate = update_data.birthdate # type: ignore

        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()


def delete_usuario(usu_id: int):
    db = None
    try:
        db = SessionLocal()
        usuario = db.query(Usuario).filter(Usuario.usu_id == usu_id).first()
        if not usuario:
            raise ValueError(f"Usuario con ID {usu_id} no encontrado")
        db.delete(usuario)
        db.commit()
        return True
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()


def authenticate_user(username: str, password: str):
    db = None
    try:
        from middlewares.auth import compare_password
        db = SessionLocal()
        usuario = db.query(Usuario).filter(Usuario.usu_usuario == username).first()
        if not usuario or not compare_password(password, str(usuario.usu_contrasenia)):
            return None
        return usuario
    finally:
        if db:
            db.close()


def login(username: str, password: str):
    db = None
    try:
        db = SessionLocal()
        usuario = db.query(Usuario).filter(Usuario.usu_usuario == username).first()
        from middlewares.auth import compare_password
        if not usuario or not compare_password(password, str(usuario.usu_contrasenia)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        # Acceder al nombre del rol dentro de la sesión
        user_type = None
        if usuario.rol:
            user_type = usuario.rol.rol_nombre
        access_token = create_access_token(data={"sub": usuario.usu_usuario, "rol_id": usuario.usu_rol_id, "user_id": usuario.usu_id})
        refresh_token = create_refresh_token(data={"sub": usuario.usu_usuario, "rol_id": usuario.usu_rol_id, "user_id": usuario.usu_id})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": usuario.usu_id,
            "username": usuario.usu_usuario,
            "user_type": user_type
        }
    finally:
        if db:
            db.close()

# Nueva función para borrar todos los usuarios
def delete_all_usuarios():
    db = None
    try:
        db = SessionLocal()
        usuarios = db.query(Usuario).all()
        for usuario in usuarios:
            db.delete(usuario)
        db.commit()
        return True
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()
