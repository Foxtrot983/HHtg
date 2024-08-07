import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'username': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASS', 'postgres'),
    'database': os.environ.get('POSTGRES_DB', 'seobot'),
}

BOT_TOKEN = os.environ.get('BOT_TOKEN')
AUTH_URL = os.environ.get('AUTH_URL')

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

APP_ACCESS_TOKEN = os.environ.get('APP_ACCESS_TOKEN')