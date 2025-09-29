from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .dto import UsuarioCreate, UsuarioOut, UsuarioUpdate, LoginResponse, LoginRequest
from .services import (
    get_all_usuarios,
    get_usuario_by_id,
    create_usuario,
    update_usuario,
    delete_usuario,
    login,
    decode_token
)

usuarios = APIRouter()

# Bearer scheme para el token JWT
bearer_scheme = HTTPBearer()


@usuarios.get("", response_model=List[UsuarioOut])
def listar_usuarios():
    """Obtener todos los usuarios"""
    print("Listando usuarios...********************************")
    try:
        users = get_all_usuarios()
        if not users:
            return []
        return users
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener los usuarios"
        )


@usuarios.get("/me")
def leer_perfil(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Devuelve los datos del usuario autenticado mediante el token JWT.
    """
    token = credentials.credentials
    payload = decode_token(token)
    return {"usuario": payload.get("sub"), "rol": payload.get("rol_id"), "user_id": payload.get("user_id")}


@usuarios.get("/{usu_id}", response_model=UsuarioOut)
def obtener_usuario(usu_id: int):
    """Obtener un usuario por ID"""
    try:
        usuario = get_usuario_by_id(usu_id)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@usuarios.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    """Crear un nuevo usuario con rol asignado"""
    try:
        return create_usuario(usuario)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="El usuario ya existe"
        )


@usuarios.patch("/{usu_id}", response_model=UsuarioOut)
def actualizar_usuario(usu_id: int, update_data: UsuarioUpdate):
    """Actualizar datos de un usuario (nombre, contraseña, rol)"""
    try:
        return update_usuario(usu_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@usuarios.delete("/{usu_id}")
def eliminar_usuario(usu_id: int):
    """Eliminar un usuario por ID"""
    try:
        if delete_usuario(usu_id):
            return {"detail": f"Usuario {usu_id} eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@usuarios.post("/login", response_model=LoginResponse)
def login_usuario(login_data: LoginRequest):
    """
    Iniciar sesión con usuario y contraseña.
    Devuelve un JWT junto con el user_id y username.
    """
    return login(login_data.username, login_data.password)
