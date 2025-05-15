from auth_service.settings.default import *

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

ACCESS_TOKEN_EXP = 300
REFRESH_TOKEN_EXP = 600

REDIS_DB = 0
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
