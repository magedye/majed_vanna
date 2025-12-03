from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

start_time = datetime.utcnow()
state: Dict[str, Optional[str]] = {
    "llm_provider": None,
    "db_provider": None,
    "port": None,
    "debug": None,
    "sqlite_path": None,
}


def update_runtime(**kwargs: Optional[str]) -> None:
    for key, value in kwargs.items():
        if key in state:
            state[key] = value


def uptime_seconds() -> float:
    return (datetime.utcnow() - start_time).total_seconds()
