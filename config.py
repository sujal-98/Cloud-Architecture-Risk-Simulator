import json
from pathlib import Path

_config_path = Path(__file__).parent / "config.json"
_config = {}

if _config_path.exists():
    with open(_config_path, "r", encoding="utf-8") as f:
        _config = json.load(f)

ITERATIONS = int(_config.get("ITERATIONS", 10000))
AVERAGE_USERS = float(_config.get("AVERAGE_USERS", 10000))
USER_STD_DEV = float(_config.get("USER_STD_DEV", 2000))
AVERAGE_REQUESTS_PER_USER = float(_config.get("AVERAGE_REQUESTS_PER_USER", 10))
COST_PER_REQUEST = float(_config.get("COST_PER_REQUEST", 0.001))

# Server configurations (lists)
SERVER_CAPACITIES = list(_config.get("SERVER_CAPACITIES", [50000, 50000, 50000]))
SERVER_FAILURE_PROBABILITIES = list(
    _config.get("SERVER_FAILURE_PROBABILITIES", [0.02, 0.02, 0.02])
)
NUMBER_OF_SERVERS = len(SERVER_CAPACITIES)

RANDOM_SEED = int(_config.get("RANDOM_SEED", 42))
