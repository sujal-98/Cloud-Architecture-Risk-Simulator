from collections import deque
from typing import Optional
from config import MAX_QUEUE_CAPACITY
from request import Request


class RequestQueue:
    """FIFO Request Queue for requests waiting for an available server."""

    def __init__(self, capacity: int = MAX_QUEUE_CAPACITY) -> None:
        self.capacity = capacity
        self._queue: deque[Request] = deque()
        self.max_depth = 0
        self.total_enqueued = 0
        self.total_dropped = 0
        self.depth_history: list[tuple[float, int]] = []

    def enqueue(self, request: Request, current_time: float) -> bool:
        """Enqueue a request if queue capacity permits."""
        if len(self._queue) >= self.capacity:
            self.total_dropped += 1
            return False

        self._queue.append(request)
        self.total_enqueued += 1

        depth = len(self._queue)
        if depth > self.max_depth:
            self.max_depth = depth

        self.depth_history.append((current_time, depth))
        return True

    def dequeue(self, current_time: float) -> Optional[Request]:
        """Dequeue the next waiting request."""
        if not self._queue:
            return None

        req = self._queue.popleft()
        self.depth_history.append((current_time, len(self._queue)))
        return req

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def __len__(self) -> int:
        return len(self._queue)
