import os
import sqlite3
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB = os.path.abspath(os.path.join(ROOT, '..', 'mise_db.db'))
UPLOADS = os.path.join(ROOT, 'static', 'uploads')

images = [f for f in os.listdir(UPLOADS) if f.lower().endswith(('.png','.jpg','.jpeg','.webp'))]
images = [f for f in images if f != 'buzo.jpeg']

sample_products = [
    ('Buzo Classic', 'Buzo cómodo y resistente', 59.99, 0.0, 'buzos-hombre'),
    ('Gorra Flex', 'Gorra estilo moderno', 19.99, 0.0, 'gorras-hombre'),
    ('Campera Invierno', 'Campera térmica para invierno', 129.9, 10.0, 'camperas-hombre'),
    ('Remera Casual', 'Remera 100% algodón', 29.5, 5.0, 'remeras-hombre'),
    ('Buzo Mujer Slim', 'Buzo para mujer corte slim', 49.99, 0.0, 'buzos-mujer'),
    ('Sombrero Vintage', 'Sombrero de cuero estilo vintage', 89.0, 15.0, 'accesorios-unisex')
]

def main():
    if not os.path.exists(DB):
        print('Database not found at', DB)
        return
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT count(*) FROM products')
    count = c.fetchone()[0]
    if count > 0:
        print('Products table already has', count, 'entries. Aborting to avoid duplicates.')
        conn.close()
        return

    print('Seeding products using images:', images)
    for i, (name, desc, price, discount, category) in enumerate(sample_products):
        img = images[i % len(images)] if images else 'buzo.jpeg'
        image_url = f'/static/uploads/{img}'
        now = datetime.utcnow().isoformat()
        c.execute('INSERT INTO products (name, description, price, image_url, discount, category) VALUES (?, ?, ?, ?, ?, ?)',
                  (name, desc, price, image_url, discount, category))
        print('Inserted', name, '->', image_url)

    conn.commit()
    conn.close()
    print('Seeding complete.')

if __name__ == '__main__':
    main()
