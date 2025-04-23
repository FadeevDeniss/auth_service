from auth_service.settings.default import *


ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
REFRESH_TOKEN_SECRET = os.environ.get('REFRESH_TOKEN_SECRET')

ACCESS_TOKEN_LIFETIME = os.environ.get('ACCESS_TOKEN_LIFETIME')
REFRESH_TOKEN_LIFETIME = os.environ.get('REFRESH_TOKEN_LIFETIME')
