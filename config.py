import os

from dotenv import load_dotenv

load_dotenv()

django_secret_key = os.getenv('DJANGO_SECRET_KEY')


database_name = os.getenv('DATABASE_NAME', 'DjangoTestDB')
database_user = os.getenv('DATABASE_USER', 'postgres')
database_password = os.getenv('DATABASE_PASSWORD', 'postgres')
database_host = os.getenv('DATABASE_HOST', 'localhost')
database_port = os.getenv('DATABASE_PORT', '5432')


email_use_tls = os.getenv('EMAIL_USE_TLS')
email_host = os.getenv('EMAIL_HOST')
email_host_user = os.getenv('EMAIL_HOST_USER')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD')
email_port = int(os.getenv('EMAIL_PORT'))