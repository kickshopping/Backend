from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio del producto (mayor a 0)")
    image_url: Optional[str] = Field(None, description="URL de la imagen del producto")
    discount: float = Field(0.0, ge=0, le=100, description="Descuento del producto (0-100%)")
    category: Optional[str] = Field(None, description="Categoría del producto (ej: hombre, mujer, ofertas)")


class ProductCreate(ProductBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nike Air Max",
                "description": "Zapatillas deportivas cómodas y elegantes",
                "price": 150.99,
                "image_url": "https://example.com/nike-air-max.jpg",
                "discount": 10.0
            }
        }


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    discount: Optional[float] = None
    category: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "price": 140.99,
                "discount": 15.0
            }
        }


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Nike Air Max",
                "description": "Zapatillas deportivas cómodas y elegantes",
                "price": 150.99,
                "image_url": "https://example.com/nike-air-max.jpg",
                "discount": 10.0
            }
        }
