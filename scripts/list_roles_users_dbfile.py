"""
Lista roles y usuarios desde la base de datos usada por la app (mise_db.db)
"""
import sqlite3

DB = 'mise_db.db'

def run():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    print('\n=== Roles ===')
    for row in cur.execute('SELECT rol_id, rol_nombre FROM roles ORDER BY rol_id'):
        print(row)
    print('\n=== Usuarios ===')
    for row in cur.execute('SELECT usu_id, usu_usuario, usu_rol_id, usu_nombre_completo FROM usuarios ORDER BY usu_id'):
        print(row)
    cur.close()
    conn.close()

if __name__ == '__main__':
    run()
