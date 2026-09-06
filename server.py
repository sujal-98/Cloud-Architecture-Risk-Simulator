from typing import Optional
from request import Request


class Server:
    """Represents a cloud server processing requests."""

    def __init__(self, server_id: int) -> None:
        self.id = server_id
        self.is_busy = False
        self.current_request: Optional[Request] = None
        self.total_busy_time = 0.0
        self.total_processed = 0
        self.last_busy_start_time = 0.0

    def assign(self, request: Request, current_time: float) -> None:
        """Assign a request to this server."""
        self.is_busy = True
        self.current_request = request
        request.start_time = current_time
        self.last_busy_start_time = current_time

    def free(self, current_time: float) -> Request:
        """Free this server upon request completion."""
        if not self.is_busy or self.current_request is None:
            raise RuntimeError(f"Server {self.id} is not busy.")

        completed_req = self.current_request
        completed_req.completion_time = current_time

        # Update server metrics
        self.total_busy_time += current_time - self.last_busy_start_time
        self.total_processed += 1

        self.is_busy = False
        self.current_request = None

        return completed_req
