import os
import shutil
import sqlite3
import random

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'mise_db.db')
DB_PATH = os.path.abspath(DB_PATH)
STATIC_UPLOADS = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
STATIC_UPLOADS = os.path.abspath(STATIC_UPLOADS)

print('DB_PATH =', DB_PATH)
print('STATIC_UPLOADS =', STATIC_UPLOADS)

# Backup DB
bak = DB_PATH + '.bak'
if not os.path.exists(bak):
    print('Creating DB backup at', bak)
    shutil.copy2(DB_PATH, bak)
else:
    print('Backup already exists at', bak)

# List image files (exclude buzo.jpeg if you want)
files = [f for f in os.listdir(STATIC_UPLOADS) if os.path.isfile(os.path.join(STATIC_UPLOADS, f))]
# Filter common image extensions
files = [f for f in files if f.lower().endswith(('.png','.jpg','.jpeg','.gif','.webp'))]
# Exclude default placeholder
files = [f for f in files if f != 'buzo.jpeg']

if not files:
    print('No candidate images found in', STATIC_UPLOADS)
    raise SystemExit(1)

print('Candidate images:', files)

# Open DB and fetch products
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('SELECT id, name, image_url FROM products')
rows = c.fetchall()
print('Found', len(rows), 'products')

if not rows:
    print('No products to update. Exiting.')
    conn.close()
    raise SystemExit(0)

# Assign images round-robin or random
for i, (pid, name, image_url) in enumerate(rows):
    chosen = random.choice(files)
    new_url = f'/static/uploads/{chosen}'
    print(f'Updating product {pid} ({name}) image: {image_url} -> {new_url}')
    c.execute('UPDATE products SET image_url = ? WHERE id = ?', (new_url, pid))

conn.commit()
conn.close()
print('Done. Database updated. Backup kept at', bak)
