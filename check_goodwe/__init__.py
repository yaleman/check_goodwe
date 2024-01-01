import os
from pathlib import Path
import sys

from pydantic import BaseModel


def ok(message: str) -> None:
    """nagios OK level"""
    print(f"OK: {message}")


def critical(message: str) -> None:
    """nagios CRITICAL level"""
    print(f"CRITICAL: {message}")
    sys.exit(2)


def unknown(message: str) -> None:
    """nagios UNKNOWN level"""
    print(f"UNKNOWN: {message}")
    sys.exit(3)


class ConfigFile(BaseModel):
    """config for check_goodwe"""

    system_id: str
    account: str
    password: str


CONFIG_FILENAME = "check_goodwe.json"

CONFIG_PATHS = [
    Path(f"./{CONFIG_FILENAME}"),
    Path(os.getenv("HOME", "./")) / f".config/{CONFIG_FILENAME}",
    Path(f"/etc/{CONFIG_FILENAME}"),
]


def load_config() -> ConfigFile:
    for filepath in CONFIG_PATHS:
        if filepath.exists():
            try:
                return ConfigFile.model_validate_json(
                    filepath.read_text(encoding="utf-8")
                )
            except Exception as error:
                print(f"Failed to load config: {error}")
                sys.exit(1)
    unknown(
        f"Couldn't find config files, tried {','.join([str(x) for x in CONFIG_PATHS])}"
    )
