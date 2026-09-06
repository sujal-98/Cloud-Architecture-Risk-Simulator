import json
from pathlib import Path

_config_path = Path(__file__).parent / "config.json"
_config = {}

if _config_path.exists():
    with open(_config_path, "r", encoding="utf-8") as f:
        _config = json.load(f)

SIMULATIONS = int(_config.get("SIMULATIONS", 1000))
HOURS_PER_SIMULATION = int(_config.get("HOURS_PER_SIMULATION", 24))
AVERAGE_USERS = float(_config.get("AVERAGE_USERS", 10000))
USER_STD_DEV = float(_config.get("USER_STD_DEV", 2000))
AVERAGE_REQUESTS_PER_USER = float(_config.get("AVERAGE_REQUESTS_PER_USER", 10))
COST_PER_SERVER_HOUR = float(_config.get("COST_PER_SERVER_HOUR", 10.0))

# Server and Autoscaling Configuration
MIN_SERVERS = int(_config.get("MIN_SERVERS", 3))
MAX_SERVERS = int(_config.get("MAX_SERVERS", 10))
DEFAULT_SERVER_CAPACITY = float(_config.get("DEFAULT_SERVER_CAPACITY", 50000))
AUTOSCALE_UP_THRESHOLD = float(_config.get("AUTOSCALE_UP_THRESHOLD", 0.80))
AUTOSCALE_DOWN_THRESHOLD = float(_config.get("AUTOSCALE_DOWN_THRESHOLD", 0.30))
SERVER_FAILURE_PROBABILITY = float(_config.get("SERVER_FAILURE_PROBABILITY", 0.01))

RANDOM_SEED = int(_config.get("RANDOM_SEED", 42))
