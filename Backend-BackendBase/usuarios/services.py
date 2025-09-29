from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from config.cnx import SessionLocal
from .model import Usuario
from .dto import UsuarioCreate, UsuarioUpdate

load_dotenv()

# Usar las mismas constantes que el middleware
SECRET_KEY = os.getenv('SECRET_KEY', default='your secret key').encode('utf-8')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
        return usuario
    finally:
        if db:
            db.close()


def create_usuario(usuario: UsuarioCreate):
    db = None
    try:
        from middlewares.auth import hash_password
        db = SessionLocal()
        nuevo_usuario = Usuario(
            usu_usuario=usuario.usu_usuario,
            usu_contrasenia=hash_password(usuario.usu_contrasenia),  
            usu_rol_id=usuario.usu_rol_id,
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
    usuario = authenticate_user(username, password)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    access_token = create_access_token(data={"sub": usuario.usu_usuario, "rol_id": usuario.usu_rol_id, "user_id": usuario.usu_id})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": usuario.usu_id,
        "username": usuario.usu_usuario
    }
