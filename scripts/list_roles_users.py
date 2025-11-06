"""
Lista roles y usuarios desde la base de datos SQLite (mise_db)
"""
import sqlite3

def run():
    conn = sqlite3.connect('mise_db')
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
