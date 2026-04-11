import json
import redis.asyncio as redis

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

    async def get(self, key: str):
        data = await self.client.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value: dict, ttl: int):
        await self.client.set(
            key,
            json.dumps(value),
            ex=ttl
        )

cache = RedisCache()