import os

import redis

redis_storage = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    db=os.environ.get('REDIS_DB', 0),
    decode_responses=True
)
