from dotenv import load_dotenv
import os

load_dotenv()
# Configuración de la base de datos
ENGINE=os.getenv('ENGINE')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
USERDB=os.getenv('USERDB')
PASSWORD=os.getenv('PASSWORD')
DATABASE=os.getenv('DATABASE')

# Cadena de conexión a la base de datos
ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')


if ENVIRONMENT == 'dev':
    strcnx = os.getenv('STRCNX')
elif ENVIRONMENT == 'qa':
    strcnx = os.getenv('STRCNXQA')
else:
    strcnx = f'{ENGINE}://{USERDB}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

STRCNX = strcnx

SQLALCHEMY_DATABASE_URI=STRCNX