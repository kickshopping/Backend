"""
Pruebas automáticas para el carrito usando TestClient y pytest.
Verifican el funcionamiento de los endpoints principales de la API.
"""

import pytest  # Importa pytest para pruebas
from fastapi.testclient import TestClient  # Cliente de pruebas para FastAPI
from config.app import app  # Importa la app principal

client = TestClient(app)  # Instancia el cliente de pruebas

def test_crear_producto():
    """
    Prueba la creación de un producto vía API.
    """
    response = client.post("/cart/products", json={
        "nombre": "Test Producto",
        "descripcion": "Producto de prueba",
        "precio": 10.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Test Producto"

def test_agregar_y_ver_carrito():
    """
    Prueba agregar un producto al carrito y consultar el carrito.
    """
    # Crear producto
    prod_resp = client.post("/cart/products", json={
        "nombre": "Test Carrito",
        "descripcion": "Producto para carrito",
        "precio": 15.0
    })
    prod_id = prod_resp.json()["id"]
    # Agregar al carrito
    add_resp = client.post("/cart/testuser/add", json={
        "product_id": prod_id,
        "cantidad": 2
    })
    assert add_resp.status_code == 200
    # Ver carrito
    cart_resp = client.get("/cart/testuser")
    assert cart_resp.status_code == 200
    cart = cart_resp.json()
    assert cart["user_id"] == "testuser"
    assert cart["total"] == 30.0

def test_remover_producto():
    """
    Prueba remover un producto del carrito y verificar el total.
    """
    # Crear producto
    prod_resp = client.post("/cart/products", json={
        "nombre": "Test Remover",
        "descripcion": "Producto para remover",
        "precio": 5.0
    })
    prod_id = prod_resp.json()["id"]
    # Agregar al carrito
    client.post("/cart/testuser2/add", json={
        "product_id": prod_id,
        "cantidad": 1
    })
    # Remover del carrito
    rem_resp = client.delete(f"/cart/testuser2/remove/{prod_id}")
    assert rem_resp.status_code == 200
    # Ver carrito vacío
    cart_resp = client.get("/cart/testuser2")
    cart = cart_resp.json()
    assert cart["total"] == 0.0

def test_vaciar_carrito():
    """
    Prueba vaciar el carrito y verificar que el total sea cero.
    """
    # Crear producto
    prod_resp = client.post("/cart/products", json={
        "nombre": "Test Vaciar",
        "descripcion": "Producto para vaciar",
        "precio": 8.0
    })
    prod_id = prod_resp.json()["id"]
    # Agregar al carrito
    client.post("/cart/testuser3/add", json={
        "product_id": prod_id,
        "cantidad": 3
    })
    # Vaciar carrito
    vaciar_resp = client.delete("/cart/testuser3/clear")
    assert vaciar_resp.status_code == 200
    # Ver carrito vacío
    cart_resp = client.get("/cart/testuser3")
    cart = cart_resp.json()
    assert cart["total"] == 0.0
