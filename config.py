from datetime import timedelta

BASE_URL_PREFIX = '/recipe/api'

JWT_AUTH_URL_RULE = f'{BASE_URL_PREFIX}/login'

JWT_EXPIRATION_DELTA = timedelta(seconds=1800)

SQLALCHEMY_TRACK_MODIFICATIONS = False

ENV = 'development'

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'recipe_db'
DB_USER = 'postgres'
DB_PWD = 'mymotog2P'

SQLALCHEMY_DATABASE_URI = f'postgres://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DEBUG = False
SECRET_KEY = '+\xba\xa5\xe6\xefv\x9c#\xba\xd9\x05pL\xc1\x11\x13\xc9\x1b-k1Rlr'

PROPOGATE_EXCEPTIONS = True

HOST_URL = 'http://localhost:5000'
