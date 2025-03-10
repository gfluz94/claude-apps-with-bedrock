from pathlib import Path
from typing import Any
import yaml


PATH_TO_CHROMA_DB = "./chroma_db"


def _read_config_file(path: Path) -> dict[str, Any]:
    with path.open("r") as file:
        return yaml.safe_load(file)
    
CONFIG: dict[str, Any] = _read_config_file(Path("config.yaml"))
