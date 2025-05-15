from auth_service.settings.default import *


ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
REFRESH_TOKEN_SECRET = os.environ.get('REFRESH_TOKEN_SECRET')

ACCESS_TOKEN_EXP = os.environ.get('ACCESS_TOKEN_EXP')
REFRESH_TOKEN_EXP = os.environ.get('REFRESH_TOKEN_EXP')
