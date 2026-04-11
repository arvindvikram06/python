import time
from fastapi import Request, Response

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.monotonic()

    def allow_request(self) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_refill

        
        self.tokens += elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens)

        self.last_refill = now

       
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        
        return False


class RateLimiter:
    def __init__(self, capacity=50, refill_rate=50/60):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = {} 

    def get_bucket(self, api_key: str) -> TokenBucket:
        if api_key not in self.buckets:
            self.buckets[api_key] = TokenBucket(
                self.capacity,
                self.refill_rate
            )
        return self.buckets[api_key]

    def is_allowed(self, api_key: str) -> bool:
        bucket = self.get_bucket(api_key)
        return bucket.allow_request()


rate_limiter = RateLimiter()