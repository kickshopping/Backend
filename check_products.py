import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'kidkshopping.db')
print('db path:', DB_PATH)

try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    print('tables:', tables)
    if 'products' in tables:
        cur.execute('SELECT count(*) FROM products')
        cnt = cur.fetchone()[0]
        print('products_count:', cnt)
        cur.execute('SELECT id, name, price FROM products LIMIT 5')
        rows = cur.fetchall()
        print('sample:', rows)
    else:
        print("'products' table not found in this database.")
except Exception as e:
    print('error querying DB:', type(e).__name__, e)
finally:
    try:
        conn.close()
    except:
        pass
