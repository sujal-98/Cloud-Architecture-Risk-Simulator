import heapq
from typing import Callable, Optional
from config import NUM_SERVERS, SIMULATION_DURATION
from events import Event, EventType
from generator import RequestGenerator
from queue import RequestQueue
from request import Request
from server import Server


class DiscreteEventEngine:
    """Discrete-Event Engine using a heapq priority queue for processing cloud request events."""

    def __init__(
        self,
        generator: RequestGenerator,
        num_servers: int = NUM_SERVERS,
        simulation_duration: float = SIMULATION_DURATION,
    ) -> None:
        self.generator = generator
        self.num_servers = num_servers
        self.simulation_duration = simulation_duration

        self.event_queue: list[Event] = []
        self.servers = [Server(i + 1) for i in range(num_servers)]
        self.request_queue = RequestQueue()

        self.completed_requests: list[Request] = []
        self.dropped_requests: list[Request] = []
        self.event_log: list[dict] = []
        self.current_time = 0.0

    def _schedule_initial_arrivals(self) -> None:
        """Schedule the first arrival event."""
        delta = self.generator.generate_next_arrival_delta()
        arrival_time = self.current_time + delta
        if arrival_time <= self.simulation_duration:
            first_req = self.generator.generate_request(arrival_time)
            heapq.heappush(
                self.event_queue,
                Event(time=arrival_time, event_type=EventType.ARRIVAL, request=first_req),
            )

    def _find_idle_server(self) -> Optional[Server]:
        """Find the first available idle server."""
        for server in self.servers:
            if not server.is_busy:
                return server
        return None

    def run(
        self,
        step_callback: Optional[Callable[[Event, float], None]] = None,
    ) -> dict:
        """Execute the discrete-event simulation loop."""
        self._schedule_initial_arrivals()

        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            if event.time > self.simulation_duration:
                break

            self.current_time = event.time

            if event.event_type == EventType.ARRIVAL:
                self._handle_arrival(event)
            elif event.event_type == EventType.COMPLETION:
                self._handle_completion(event)

            if step_callback:
                step_callback(event, self.current_time)

        return {
            "completed_requests": self.completed_requests,
            "dropped_requests": self.dropped_requests,
            "servers": self.servers,
            "queue": self.request_queue,
            "total_simulation_time": self.current_time,
            "event_log": self.event_log,
        }

    def _handle_arrival(self, event: Event) -> None:
        req = event.request
        idle_server = self._find_idle_server()

        if idle_server is not None:
            # Server is available immediately -> Assign request and schedule completion event
            idle_server.assign(req, self.current_time)
            completion_time = self.current_time + req.service_time
            heapq.heappush(
                self.event_queue,
                Event(
                    time=completion_time,
                    event_type=EventType.COMPLETION,
                    request=req,
                    server=idle_server,
                ),
            )
            self.event_log.append({
                "time": self.current_time,
                "event": "ARRIVAL_ASSIGNED",
                "req_id": req.id,
                "server_id": idle_server.id,
            })
        else:
            # All servers busy -> Push to request queue
            enqueued = self.request_queue.enqueue(req, self.current_time)
            if not enqueued:
                self.dropped_requests.append(req)
                self.event_log.append({
                    "time": self.current_time,
                    "event": "ARRIVAL_DROPPED",
                    "req_id": req.id,
                })
            else:
                self.event_log.append({
                    "time": self.current_time,
                    "event": "ARRIVAL_QUEUED",
                    "req_id": req.id,
                    "queue_depth": len(self.request_queue),
                })

        # Schedule next request arrival if within simulation duration limit
        next_delta = self.generator.generate_next_arrival_delta()
        next_arrival_time = self.current_time + next_delta
        if next_arrival_time <= self.simulation_duration:
            next_req = self.generator.generate_request(next_arrival_time)
            heapq.heappush(
                self.event_queue,
                Event(
                    time=next_arrival_time,
                    event_type=EventType.ARRIVAL,
                    request=next_req,
                ),
            )

    def _handle_completion(self, event: Event) -> None:
        server = event.server
        if server is None:
            return

        completed_req = server.free(self.current_time)
        self.completed_requests.append(completed_req)

        self.event_log.append({
            "time": self.current_time,
            "event": "COMPLETION",
            "req_id": completed_req.id,
            "server_id": server.id,
            "latency": completed_req.latency,
            "waiting_time": completed_req.waiting_time,
        })

        # Check if there are waiting requests in the queue
        if not self.request_queue.is_empty():
            next_req = self.request_queue.dequeue(self.current_time)
            if next_req:
                server.assign(next_req, self.current_time)
                completion_time = self.current_time + next_req.service_time
                heapq.heappush(
                    self.event_queue,
                    Event(
                        time=completion_time,
                        event_type=EventType.COMPLETION,
                        request=next_req,
                        server=server,
                    ),
                )
                self.event_log.append({
                    "time": self.current_time,
                    "event": "DEQUEUED_ASSIGNED",
                    "req_id": next_req.id,
                    "server_id": server.id,
                    "waiting_time": next_req.waiting_time,
                })
