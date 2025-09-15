from dotenv import load_dotenv
import os

load_dotenv()

# Cadena de conexión a la base de datos
STRCNX = os.getenv('STRCNX')

# Configuración de la base de datos
ENGINE = os.getenv('ENGINE')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
USERDB = os.getenv('USERDB')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

# Si querés armar la cadena de conexión manualmente (por si STRCNX no existe):
if not STRCNX:
    # Ejemplo para SQLite:
    # STRCNX = f"sqlite:///./kickshopping.db"
    # Ejemplo para PostgreSQL:
    # STRCNX = f"postgresql://{USERDB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    if ENGINE == "sqlite":
        STRCNX = f"sqlite:///./kickshopping.db"
    else:
        STRCNX = f"{ENGINE}://{USERDB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

SQLALCHEMY_DATABASE_URL = STRCNX
