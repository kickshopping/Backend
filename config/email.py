import os

# Configuración de email vía variables de entorno
SMTP_HOST = os.environ.get('SMTP_HOST', 'localhost')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '1025'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', 'False').lower() in ('1', 'true', 'yes')

# Dirección desde la que se envían los correos
EMAIL_FROM = os.environ.get('EMAIL_FROM', 'no-reply@example.com')

# Destinatarios por defecto (coma-separados). Puedes establecer PURCHASE_EMAILS="a@gmail.com,b@gmail.com"
PURCHASE_EMAILS = os.environ.get('PURCHASE_EMAILS', 'laureano24gonzalez@gmail.com')
