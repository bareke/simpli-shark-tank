from os import getenv
from dotenv import load_dotenv

load_dotenv()

settings = {
    'ia_apikey': getenv('IA_APIKEY'),

    'db_host': getenv('DB_HOST'),
    'db_name': getenv('DB_NAME'),
    'db_user': getenv('DB_USER'),
    'db_password': getenv('DB_PASSWORD'),
    'db_port': getenv('DB_PORT')
}
