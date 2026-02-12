import time
from collections import defaultdict, deque
from app.config import settings

class RateLimiter:
    """
    Simple in-memory limiter for MVP.
    Enterprise upgrade: replace with Redis/KeyDB to support multiple instances.
    """
    def __init__(self):
        self.client_events = defaultdict(deque)
        self.ip_events = defaultdict(deque)

    def _prune(self, q: deque, now: float):
        window_start = now - 60
        while q and q[0] < window_start:
            q.popleft()

    def allow(self, client_id: str, ip: str) -> bool:
        now = time.time()

        # Per-client key limit
        cq = self.client_events[client_id]
        self._prune(cq, now)
        if len(cq) >= settings.max_requests_per_minute:
            return False
        cq.append(now)

        # Per-IP limit
        iq = self.ip_events[ip]
        self._prune(iq, now)
        if len(iq) >= settings.max_requests_per_minute:
            return False
        iq.append(now)

        return True

rate_limiter = RateLimiter()
