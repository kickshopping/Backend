from dotenv import load_dotenv
import os

load_dotenv()

# Configuración de la base de datos (leer variables, con nombres alternativos donde aplique)
ENGINE = os.getenv('ENGINE')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
# algunas .env usan USERDB, otras USER
USERDB = os.getenv('USERDB') or os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

# Cadena de conexión a la base de datos
ENVIROMENT = os.getenv('ENVIROMENT', 'prod')

# Preferir si STRCNX ya está definida (útil en dev)
STRCNX_ENV = os.getenv('STRCNX')
STRCNX_QA = os.getenv('STRCNXQA')
# Seguridad / JWT
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '30'))

# Asegurarnos de que SECRET_KEY esté definida (usar valor por defecto en desarrollo)
if not SECRET_KEY:
    # No bloquear la importación en entornos locales; usar una clave por defecto y avisar
    SECRET_KEY = 'dev-secret-change-me'
    print("[config] WARNING: SECRET_KEY no está definida en .env — usando clave por defecto de desarrollo")

# Preferencia local: si existe kidkshopping.db en el proyecto, usarlo por defecto
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KID_DB_PATH = PROJECT_ROOT / 'kidkshopping.db'

if STRCNX_ENV and ENVIROMENT == 'dev':
    STRCNX = STRCNX_ENV
elif STRCNX_QA and ENVIROMENT == 'qa':
    STRCNX = STRCNX_QA
else:
    # Si el motor es sqlite, construir una URL válida para sqlite
    if ENGINE and ENGINE.lower() in ('sqlite', 'sqlite3'):
        # Si DATABASE ya es una ruta (contiene '/' o '\\' o termina en .db), usarla tal cual
        if DATABASE and ("/" in DATABASE or "\\" in DATABASE or DATABASE.endswith('.db')):
            # Asegurar que la URL tenga 3 o 4 slashes según sea relativo o absoluto
            if DATABASE.startswith('/') or (len(DATABASE) > 1 and DATABASE[1] == ':'):
                STRCNX = f'sqlite:///{DATABASE}'
            else:
                STRCNX = f'sqlite:///{DATABASE}'
        else:
            # Crear archivo local con extensión .db si falta
            db_name = DATABASE or 'database'
            if not db_name.endswith('.db'):
                db_name = f"{db_name}.db"
            STRCNX = f'sqlite:///{db_name}'
    else:
        # Si no se indicó ENGINE, preferir fallback sqlite local en vez de crear
        # una URL inválida como 'None://...'. Esto evita que SQLAlchemy intente
        # cargar un dialecto llamado 'None'.
        if not ENGINE:
            default_db = PROJECT_ROOT / 'kikshopping.db'
            STRCNX = f"sqlite:///{default_db}"
        else:
            # Construir cadena tipo dialect+driver://user:pass@host:port/db
            # Intentar no incluir credenciales vacías
            user = USERDB or ''
            pwd = PASSWORD or ''
            host = HOST or 'localhost'
            port = PORT or ''
            db = DATABASE or ''
            # Forma base
            if user:
                auth = f"{user}:{pwd}@"
            else:
                auth = ''
            hostport = f"{host}:{port}" if port else host
            STRCNX = f"{ENGINE}://{auth}{hostport}/{db}"

SQLALCHEMY_DATABASE_URI = STRCNX

# Si no se definió STRCNX vía envs de dev/qa, preferir el kidkshopping.db local cuando exista
try:
    if (not STRCNX_ENV) and (not STRCNX_QA) and KID_DB_PATH.exists():
        STRCNX = f"sqlite:///{str(KID_DB_PATH.resolve())}"
        SQLALCHEMY_DATABASE_URI = STRCNX
        print(f"[config] Overriding STRCNX to local DB: {KID_DB_PATH.resolve()}")
except Exception:
    # No bloquear si hay problemas con filesystem; dejar STRCNX tal como quedó
    pass

# Fallback default si STRCNX no fue correctamente configurada
if 'STRCNX' not in globals() or not STRCNX:
    default_db = PROJECT_ROOT / 'kikshopping.db'
    STRCNX = f"sqlite:///{default_db}"
    SQLALCHEMY_DATABASE_URI = STRCNX
    print(f"[config] INFO: STRCNX no configurado, usando DB por defecto: {default_db}")
