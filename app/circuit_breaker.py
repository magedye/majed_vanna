import time
from typing import Callable, Awaitable, Any


class CircuitBreaker:
    def __init__(
        self,
        name: str,
        failure_threshold: int = 3,
        reset_timeout: int = 30,
        half_open_success: int = 1,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.half_open_success = half_open_success
        self.state = "CLOSED"
        self.failures = 0
        self.last_failure = 0
        self.successes = 0

    def _can_pass(self) -> bool:
        if self.state == "OPEN":
            if time.time() - self.last_failure >= self.reset_timeout:
                self.state = "HALF_OPEN"
                self.successes = 0
                return True
            return False
        return True

    def _on_success(self):
        self.failures = 0
        if self.state == "HALF_OPEN":
            self.successes += 1
            if self.successes >= self.half_open_success:
                self.state = "CLOSED"
        else:
            self.state = "CLOSED"

    def _on_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"

    async def call_async(self, func: Callable[[], Any]):
        if not self._can_pass():
            raise RuntimeError(f"CircuitBreaker[{self.name}] is OPEN")
        try:
            result = func()
            if hasattr(result, "__await__"):
                result = await result
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise
