from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración de la base de datos
DATABASE = os.getenv('DATABASE', 'kikshopping.db')
ENGINE = os.getenv('ENGINE', 'sqlite')

# Si es sqlite, construir la URL apropiada
if ENGINE.lower() in ('sqlite', 'sqlite3'):
    db_path = Path(DATABASE)
    if not db_path.is_absolute():
        # Hacer la ruta relativa al directorio del proyecto
        db_path = Path(__file__).parent.parent / DATABASE
    DATABASE_URL = f'sqlite:///{db_path}'
else:
    # Para otros motores como PostgreSQL, MySQL, etc.
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    USER = os.getenv('USER') 
    PASSWORD = os.getenv('PASSWORD')
    DATABASE_URL = f"{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"