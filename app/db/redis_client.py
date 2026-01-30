import redis
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def cache_set(key: str, value: str, expire_seconds: int = 300):
    redis_client.set(key, value, ex=expire_seconds)

def cache_get(key: str):
    return redis_client.get(key)
