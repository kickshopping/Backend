import requests

# Cambia la URL si tu backend corre en otra IP o puerto
url = "http://localhost:8000/productos/"

productos = [
    {
        "name": "Nike Air Max",
        "description": "Zapatillas deportivas cómodas y elegantes",
        "price": 150.99,
        "image_url": "https://example.com/nike-air-max.jpg",
        "discount": 10.0
    },
    {
        "name": "Adidas Superstar",
        "description": "Clásicas y urbanas",
        "price": 120.50,
        "image_url": "https://example.com/adidas-superstar.jpg",
        "discount": 5.0
    },
    {
        "name": "Puma RS-X",
        "description": "Estilo retro y moderno",
        "price": 135.00,
        "image_url": "https://example.com/puma-rsx.jpg",
        "discount": 0.0
    }
]

for producto in productos:
    response = requests.post(url, json=producto)
    if response.status_code == 201:
        print(f"Producto '{producto['name']}' cargado correctamente.")
    else:
        print(f"Error al cargar '{producto['name']}':", response.text)
