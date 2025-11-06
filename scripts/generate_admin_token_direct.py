"""
Genera un token JWT directamente usando SECRET_KEY sin importar modelos.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.auth import SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta, timezone
from jose import jwt


def gen():
    now = datetime.now(timezone.utc)
    exp = int((now + timedelta(minutes=600)).timestamp())
    payload = {
        'sub': 'admin@gmail.com',
        'rol_id': 1,
        'user_id': 1,
        'exp': exp
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print('\n=== Token generado ===')
    print(token)
    print('\n=== Payload decodificado ===')
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(decoded)

if __name__ == '__main__':
    gen()
