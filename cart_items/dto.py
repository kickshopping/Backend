from pydantic import BaseModel, Field
from typing import Optional


class CartItemBase(BaseModel):
    user_id: int = Field(..., gt=0, description="ID del usuario")
    product_id: int = Field(..., gt=0, description="ID del producto")
    quantity: int = Field(1, gt=0, description="Cantidad del producto (mínimo 1)")


class CartItemCreate(CartItemBase):
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "product_id": 1,
                "quantity": 2
            }
        }


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0, description="Cantidad del producto (mínimo 1)")

    class Config:
        json_schema_extra = {
            "example": {
                "quantity": 3
            }
        }


class CartItemOut(CartItemBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "product_id": 1,
                "quantity": 2
            }
        }


# DTOs con información extendida incluyendo detalles del usuario y producto
class UserSimple(BaseModel):
    usu_id: int
    usu_usuario: str
    usu_nombre_completo: str

    class Config:
        from_attributes = True


class ProductSimple(BaseModel):
    id: int
    name: str
    price: float
    image_url: Optional[str] = None
    description: Optional[str] = None
    discount: Optional[float] = 0.0

    class Config:
        from_attributes = True


class CartItemOutDetailed(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    user: Optional[UserSimple] = None
    product: Optional[ProductSimple] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "product_id": 1,
                "quantity": 2,
                "user": {
                    "usu_id": 1,
                    "usu_usuario": "john123",
                    "usu_nombre_completo": "John Doe"
                },
                "product": {
                    "id": 1,
                    "name": "Nike Air Max",
                    "price": 150.99,
                    "image_url": "https://example.com/nike-air-max.jpg",
                    "description": "Zapatillas deportivas premium",
                    "discount": 0.0
                }
            }
        }