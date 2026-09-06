from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class EventType(Enum):
    """Discrete Event types."""

    ARRIVAL = 1
    COMPLETION = 2


@dataclass(order=True)
class Event:
    """Discrete Event ordered by timestamp for heapq priority queue execution."""

    time: float
    event_type: EventType = field(compare=False)
    request: Any = field(compare=False)
    server: Optional[Any] = field(default=None, compare=False)
