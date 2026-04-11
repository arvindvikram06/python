import time


class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_time=30):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None

    def can_request(self):
        if self.state == "OPEN":
            now = time.monotonic()
            if now - self.last_failure_time > self.recovery_time:
                self.state = "HALF_OPEN"
                return True

            return False

        return True

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.monotonic()

        if self.failures >= self.failure_threshold:
            self.state = "OPEN"

class CircuitBreakerManager:
    def __init__(self):
        self.breakers = {}

    def get_breaker(self, service_name):
        if service_name not in self.breakers:
            self.breakers[service_name] = CircuitBreaker()
        return self.breakers[service_name]


circuit_manager = CircuitBreakerManager()