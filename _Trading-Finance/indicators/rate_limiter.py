"""
Rate Limiter — prevents API throttling with token bucket algorithm.

From Repo A: 2 calls/sec with exponential backoff on 429/5xx errors.
Thread-safe, reusable across any API client.
"""

from __future__ import annotations
import time
import threading
from typing import Optional


class RateLimiter:
    """Token bucket rate limiter.

    Parameters:
        calls_per_second:  max API calls per second (default 2)
        burst:             max burst size (default = calls_per_second)
    """

    def __init__(self, calls_per_second: float = 2.0, burst: Optional[int] = None):
        self.rate = calls_per_second
        self.burst = burst or int(calls_per_second)
        self._tokens = float(self.burst)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self, timeout: float = 10.0) -> bool:
        """Wait until a token is available, then consume it.

        Returns True if acquired, False if timed out.
        """
        deadline = time.monotonic() + timeout
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return True

            if time.monotonic() >= deadline:
                return False
            time.sleep(0.05)  # 50ms polling

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self.burst, self._tokens + elapsed * self.rate)
        self._last_refill = now

    @property
    def available_tokens(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens


def exponential_backoff(attempt: int, base: float = 1.0, max_delay: float = 30.0) -> float:
    """Calculate backoff delay: base * 2^attempt, capped at max_delay."""
    delay = base * (2 ** attempt)
    return min(delay, max_delay)
