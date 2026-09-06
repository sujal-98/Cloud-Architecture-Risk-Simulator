import json
from pathlib import Path

_config_path = Path(__file__).parent / "config.json"
_config = {}

if _config_path.exists():
    with open(_config_path, "r", encoding="utf-8") as f:
        _config = json.load(f)

SIMULATION_DURATION = float(_config.get("SIMULATION_DURATION", 100.0))
ARRIVAL_RATE = float(_config.get("ARRIVAL_RATE", 50.0))  # requests per second
AVG_SERVICE_TIME = float(_config.get("AVG_SERVICE_TIME", 0.05))  # seconds per request
NUM_SERVERS = int(_config.get("NUM_SERVERS", 3))
MAX_QUEUE_CAPACITY = int(_config.get("MAX_QUEUE_CAPACITY", 1000))
RANDOM_SEED = int(_config.get("RANDOM_SEED", 42))
