import sys, json, time
sys.path.insert(0, r'C:\Users\Thiago\Desktop\eflksnkose\backend-kikshopping')
from fastapi.testclient import TestClient
import main
client = TestClient(main.app)
email = f'test_user_{int(time.time())}@example.com'
create_payload = {
    'email': email,
    'first_name': 'Test',
    'last_name': 'User',
    'password': 'password123',
}
print('Creating user', email)
r = client.post('/usuarios', json=create_payload)
print('CREATE status', r.status_code, 'body', r.text)
if r.status_code==201:
    tokens = r.json()
    access = tokens.get('access_token')
    print('Got access token length', len(access) if access else None)
    # Call /usuarios/me with Authorization and Origin
    headers = {'Authorization': f'Bearer {access}', 'Origin': 'http://localhost:3000'}
    r2 = client.get('/usuarios/me', headers=headers)
    print('ME status', r2.status_code)
    print('ME headers', json.dumps(dict(r2.headers), ensure_ascii=False))
    print('ME body', r2.text)
else:
    print('Create failed; try login if user exists')
    # attempt login
    login_payload = {'username': email, 'password': 'password123'}
    r3 = client.post('/usuarios/login', json=login_payload)
    print('LOGIN status', r3.status_code, r3.text)
