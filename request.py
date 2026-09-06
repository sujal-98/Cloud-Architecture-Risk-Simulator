from dataclasses import dataclass
from typing import Optional


@dataclass
class Request:
    """Represents a cloud request undergoing discrete-event simulation."""

    id: int
    arrival_time: float
    service_time: float
    start_time: Optional[float] = None
    completion_time: Optional[float] = None

    @property
    def waiting_time(self) -> float:
        """Time spent waiting in the queue before processing starts."""
        if self.start_time is None:
            return 0.0
        return self.start_time - self.arrival_time

    @property
    def latency(self) -> float:
        """Total time from arrival to completion (Waiting Time + Service Time)."""
        if self.completion_time is None:
            return 0.0
        return self.completion_time - self.arrival_time
