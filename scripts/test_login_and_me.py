"""
Hace login y luego llama a /usuarios/me para verificar rol en el backend.
"""
import json
import sys
from urllib import request, error

API = 'http://localhost:8000'
LOGIN_URL = API + '/usuarios/login'
ME_URL = API + '/usuarios/me'

creds = {'username': 'admin@gmail.com', 'password': 'admin123'}

def do_login():
    payload = json.dumps(creds).encode('utf-8')
    req = request.Request(LOGIN_URL, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
    with request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def do_me(token):
    req = request.Request(ME_URL, headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'})
    with request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


try:
    login_resp = do_login()
    print('Login response:')
    print(json.dumps(login_resp, indent=2, ensure_ascii=False))
    token = login_resp.get('access_token')
    if token:
        me = do_me(token)
        print('\n/me response:')
        print(json.dumps(me, indent=2, ensure_ascii=False))
    else:
        print('No access_token in login response')
except error.HTTPError as e:
    print('HTTP Error:', e.code, e.reason)
    try:
        print(e.read().decode())
    except Exception:
        pass
except Exception as e:
    print('Error:', e)
    sys.exit(1)
