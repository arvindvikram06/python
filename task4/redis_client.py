import redis
from config import REDIS_HOST

r = redis.Redis(host=REDIS_HOST, decode_responses=True)