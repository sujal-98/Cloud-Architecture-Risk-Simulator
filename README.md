# Discrete-Event Cloud Request Processing Simulator

An event-driven, discrete-event cloud simulator for modeling request latencies, queuing behaviors, server utilization, and throughput using Python's `heapq` priority queue.

---

## Architecture & Design

The simulator follows a **Discrete-Event Simulation (DES)** architecture:

```text
Request Generator (Poisson Arrival & Service Times)
       │
       ▼
 ┌───────────┐
 │ Event     │ (Priority Queue via heapq)
 │ Queue     │
 └─────┬─────┘
       │
       ▼
 ┌───────────┐
 │ Discrete  │
 │ Event     │
 │ Engine    │
 └─────┬─────┘
       │
       ├──────────────────────────┐
       ▼                          ▼
 ┌───────────┐              ┌───────────┐
 │ Request   │ (FIFO Queue) │ Cloud     │
 │ Queue     │              │ Servers   │
 └───────────┘              └─────┬─────┘
                                  │
                                  ▼
                         Request Completion
```

### Request Lifecycle & Latency Calculation:

$$\text{Latency} = \text{Completion Time} - \text{Arrival Time} = \text{Waiting Time} + \text{Service Time}$$

- **Arrival Event**: The engine assigns the incoming request to an idle server. If all servers are busy, the request enters the FIFO queue.
- **Completion Event**: The server finishes processing, frees itself, and immediately picks up the next request waiting in the queue.

---

## Features

- **Discrete-Event Priority Queue**: Events are processed in strict chronological order using `heapq`.
- **Latency Percentiles**: Calculates **P50 (Median)**, **P95**, **P99**, and **Maximum** request latencies.
- **Queue Depth & Waiting Time Tracking**: Measures queue buildup, maximum queue depth, and waiting times.
- **Live Matplotlib Dashboard**: Streams real-time updates for:
  - Latency Distribution (with P50, P95, P99 markers)
  - Queue Depth Timeline over simulation time
  - Per-Server Utilization Bar Chart
  - Queue Waiting Time Distribution

---

## Project Structure

```text
monte-carlo-simulation/
├── config.json       # Configurable simulation parameters
├── config.py         # Configuration loader
├── events.py         # Priority queue Event structures (ARRIVAL, COMPLETION)
├── request.py        # Request state tracking (arrival, start, completion, latency)
├── server.py         # Server state and utilization tracking
├── queue.py          # FIFO Request Queue implementation
├── generator.py      # Stochastic Poisson arrival & service time generator
├── engine.py         # Discrete-Event Priority Queue Engine (heapq)
├── metrics.py        # Metrics calculator (P50, P95, P99, Throughput, Utilization)
├── visualization.py  # Live-updating 4-panel Matplotlib dashboard
├── main.py           # Main orchestration entry point
├── .gitignore        # Version control exclusions
└── README.md         # Project documentation
```

---

## Configuration (`config.json`)

```json
{
  "SIMULATION_DURATION": 100.0,
  "ARRIVAL_RATE": 50.0,
  "AVG_SERVICE_TIME": 0.05,
  "NUM_SERVERS": 3,
  "MAX_QUEUE_CAPACITY": 1000,
  "RANDOM_SEED": 42
}
```

- **`SIMULATION_DURATION`**: Total simulation run time in seconds.
- **`ARRIVAL_RATE`**: Average incoming request arrival rate ($\lambda$ requests/second).
- **`AVG_SERVICE_TIME`**: Mean processing duration per request (seconds).
- **`NUM_SERVERS`**: Number of available processing servers in the cluster pool.
- **`MAX_QUEUE_CAPACITY`**: Maximum waiting queue depth before requests are dropped.

---

## Getting Started

### Prerequisites

- Python 3.10+
- `numpy`
- `matplotlib`

### Installation

```bash
pip install numpy matplotlib
```

### Running the Simulator

Execute the simulation by running:

```bash
python main.py
```

---

## Sample Output

```text
===========================================================================
  Discrete-Event Cloud Request Processing Simulator
===========================================================================
Simulation Duration : 100.0 seconds
Arrival Rate        : 50.0 requests/second
Avg Service Time    : 50.0 ms
Server Pool Size    : 3 servers
===========================================================================

Sample Event Execution Trace (First 15 Events):
Time (s)   Event                Req ID   Server     Latency (ms)   
───────────────────────────────────────────────────────────────────────────
0.0132     ARRIVAL_ASSIGNED     R1       Server 1   -              
0.0274     ARRIVAL_ASSIGNED     R2       Server 2   -              
0.0315     ARRIVAL_ASSIGNED     R3       Server 3   -              
0.0541     ARRIVAL_QUEUED       R4       -          -              
0.0612     COMPLETION           R1       Server 1     48.00 ms     
0.0612     DEQUEUED_ASSIGNED    R4       Server 1   -              
───────────────────────────────────────────────────────────────────────────

===========================================================================
  SIMULATION METRICS & LATENCY SUMMARY
===========================================================================
Total Requests Processed : 4,982
Total Requests Dropped   : 0
Throughput               : 49.82 requests/sec
Overall Cluster Util.    : 83.14%
───────────────────────────────────────────────────────────────────────────
Average Latency          : 85.32 ms
P50 Latency (Median)     : 64.12 ms
P95 Latency              : 198.45 ms
P99 Latency              : 284.10 ms
Max Latency              : 412.50 ms
───────────────────────────────────────────────────────────────────────────
Average Waiting Time     : 35.20 ms
P95 Waiting Time         : 148.10 ms
Max Queue Depth          : 18 requests
───────────────────────────────────────────────────────────────────────────
Per-Server Utilization:
  Server 1: Processed 1,670 requests (84.1% busy)
  Server 2: Processed 1,658 requests (82.9% busy)
  Server 3: Processed 1,654 requests (82.4% busy)
===========================================================================
```
