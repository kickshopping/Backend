from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Request, Depends
import os
import uuid
import shutil
from typing import List
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .dto import ProductCreate, ProductOut, ProductUpdate
from .services import (
    get_all_products, 
    get_product_by_id, 
    create_product, 
    update_product, 
    delete_product,
    get_products_by_category
)
from middlewares.admin_auth import verify_admin
from usuarios.model import Usuario

products = APIRouter()

@products.get('/categoria/{category}', response_model=List[ProductOut])
def list_products_by_category(category: str):
    """Obtener productos por categoría"""
    try:
        return get_products_by_category(category)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor al obtener los productos: {str(e)}"
        )

@products.get('', response_model=List[ProductOut], status_code=status.HTTP_200_OK)
def get_products():
    """Obtener todos los productos"""
    try:
        return get_all_products()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener los productos"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener los productos"
        )

@products.get('/{product_id}', response_model=ProductOut, status_code=status.HTTP_200_OK)
def get_product(product_id: int):
    """Obtener un producto por ID"""
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID del producto debe ser un numero positivo"
            )
        
        product = get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        return product
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener el producto"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener el producto"
        )

@products.post('', response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def post_product(product: ProductCreate, admin: Usuario = Depends(verify_admin)):
    """Crear un nuevo producto"""
    try:
        if not product.name or product.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Datos inválidos: nombre requerido, precio > 0"
            )
        
        return create_product(product)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error de integridad de datos al crear el producto"
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al crear el producto"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al crear el producto"
        )


@products.post('/upload', response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def upload_product(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    description: str | None = Form(None),
    discount: float | None = Form(0.0),
    category: str | None = Form(None),
    file: UploadFile = File(...),
):
    """Subir una imagen y crear un producto (multipart/form-data)"""
    try:
        # Ensure uploads directory exists
        base_dir = os.path.join(os.getcwd(), 'static', 'uploads')
        os.makedirs(base_dir, exist_ok=True)

        # Create a safe unique filename
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(base_dir, filename)

        # Save the uploaded file to disk
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(file.file, out_file)

        # Build a public URL for the saved file (served under /static)
        image_url = f"/static/uploads/{filename}"

        # Create product using existing service
        product_data = ProductCreate(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            discount=discount or 0.0,
            category=category,
        )

        return create_product(product_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir el archivo y crear el producto: {str(e)}"
        )

@products.post('/{product_id}/imagen', response_model=ProductOut)
async def update_product_image(
    product_id: int,
    file: UploadFile = File(...),
    admin: Usuario = Depends(verify_admin)
):
    """Actualizar la imagen de un producto existente"""
    try:
        # Ensure uploads directory exists
        base_dir = os.path.join(os.getcwd(), 'static', 'uploads')
        os.makedirs(base_dir, exist_ok=True)

        # Create a safe unique filename
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(base_dir, filename)

        # Save the uploaded file to disk
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(file.file, out_file)

        # Build a public URL for the saved file
        image_url = f"/static/uploads/{filename}"

        # Update product with new image URL
        # Get the current product first
        product = get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
            
        # Just update the image_url
        update_data = ProductUpdate(image_url=image_url)
        updated = update_product(product_id, update_data)

        # Attempt to remove the previous image file from disk to avoid orphaned files
        try:
            old_url = getattr(product, 'image_url', '') or ''
            # Only delete files that live under /static/uploads/
            prefix = '/static/uploads/'
            if isinstance(old_url, str) and old_url.startswith(prefix):
                old_filename = old_url[len(prefix):]
                # Ensure we don't accidentally delete the file we just saved
                old_filename = str(old_filename)
                if old_filename and old_filename != filename:
                    old_path = os.path.join(os.getcwd(), 'static', 'uploads', old_filename)
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except Exception:
                            # ignore failures to delete; it's not fatal for the request
                            pass
        except Exception:
            # ignore any errors deleting the old file
            pass

        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la imagen del producto: {str(e)}"
        )

@products.patch('/{product_id}', response_model=ProductOut, status_code=status.HTTP_200_OK)
def patch_product(product_id: int, update_data: ProductUpdate, admin: Usuario = Depends(verify_admin)):
    """Actualizar campos de un producto existente"""
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de producto debe ser un numero positivo"
            )
    
        return update_product(product_id, update_data)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al actualizar el producto"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al actualizar el producto"
        )
    
@products.delete('/{product_id}', status_code=status.HTTP_200_OK)
def delete_product_route(product_id: int, admin: Usuario = Depends(verify_admin)):
    """Eliminar un producto por ID"""
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de producto debe ser un numero positivo"
            )
        
        eliminado = delete_product(product_id)
        if not eliminado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )
        return {"detail": f"Producto con ID {product_id} eliminado exitosamente"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al eliminar el producto"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al eliminar el producto"
        )
    