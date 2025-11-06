from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class UsuarioBase(BaseModel):
    usu_usuario: str
    usu_nombre_completo: str
    tipo_usuario: str = Field(..., description="Tipo de usuario: 'Vendedor' o 'Comprador'")
    birthdate: Optional[date] = Field(None, description="Fecha de nacimiento del usuario")


class UsuarioCreate(UsuarioBase):
    usu_contrasenia: str

    class Config:
        json_schema_extra = {
            "example": {
                "usu_usuario": "john123",
                "usu_nombre_completo": "John Doe",
                "usu_contrasenia": "Secreta123",
                "usu_rol_id": 2,
                "birthdate": "1995-03-15"
            }
        }


class UsuarioUpdate(BaseModel):
    usu_nombre_completo: Optional[str] = None
    usu_contrasenia: Optional[str] = None
    usu_rol_id: Optional[int] = None
    birthdate: Optional[date] = None

    class Config:
        json_schema_extra = {
            "example": {
                "usu_nombre_completo": "John D.",
                "usu_contrasenia": "Clave456",
                "usu_rol_id": 1,
                "birthdate": "1995-03-15"
            }
        }



class UsuarioOut(UsuarioBase):
    usu_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "usu_id": 1,
                "usu_usuario": "john123",
                "usu_nombre_completo": "John Doe",
                "usu_rol_id": 2,
                "birthdate": "1995-03-15",
                "created_at": "2025-09-11T12:00:00"
            }
        }


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    user_type: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": 1,
                "username": "john123"
            }
        }
