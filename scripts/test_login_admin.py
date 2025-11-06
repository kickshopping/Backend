"""
Intenta iniciar sesión en el backend con admin@gmail.com / admin123 y muestra la respuesta.
"""
import json
import sys
from urllib import request, error

API = 'http://localhost:8000'
LOGIN_URL = API + '/usuarios/login'

payload = json.dumps({'username': 'admin@gmail.com', 'password': 'admin123'}).encode('utf-8')
req = request.Request(LOGIN_URL, data=payload, headers={'Content-Type': 'application/json'}, method='POST')

try:
    with request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
        print('Status:', resp.status)
        try:
            data = json.loads(body)
            print('Response JSON:')
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception:
            print('Response body:', body)
        # If token present, decode payload without verification
        if isinstance(data, dict) and data.get('access_token'):
            token = data['access_token']
            print('\nAccess token (compact):', token)
            try:
                # decode token payload (base64url)
                import base64
                parts = token.split('.')
                if len(parts) >= 2:
                    b = parts[1]
                    # add padding
                    b += '=' * (-len(b) % 4)
                    decoded = base64.urlsafe_b64decode(b.encode('utf-8'))
                    print('Decoded payload:')
                    print(json.dumps(json.loads(decoded), indent=2, ensure_ascii=False))
                else:
                    print('Token format unexpected')
            except Exception as e:
                print('Could not decode token payload:', e)

except error.HTTPError as e:
    print('HTTP Error:', e.code, e.reason)
    try:
        print(e.read().decode())
    except Exception:
        pass
except Exception as e:
    print('Error connecting to backend:', e)
    sys.exit(1)
