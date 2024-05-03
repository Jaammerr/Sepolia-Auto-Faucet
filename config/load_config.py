import os
import yaml

from loguru import logger
from models import Config


def get_accounts() -> list[str]:
    accounts_path = os.path.join(os.path.dirname(__file__), "accounts.txt")
    if not os.path.exists(accounts_path):
        logger.error(f"File <<{accounts_path}>> does not exist")
        exit(1)

    with open(accounts_path, "r") as f:
        accounts = f.readlines()

        if not accounts:
            logger.error(f"File <<{accounts_path}>> is empty")
            exit(1)

        return accounts


def load_config() -> Config:
    settings_path = os.path.join(os.path.dirname(__file__), "settings.yaml")
    if not os.path.exists(settings_path):
        logger.error(f"File <<{settings_path}>> does not exist")
        exit(1)

    with open(settings_path, "r") as f:
        settings = yaml.safe_load(f)

    REQUIRED_KEYS = (
        "threads",
        "min_amount",
        "max_amount",
        "arb_rpc",
        "delay_before_start_min",
        "delay_before_start_max",
    )

    for key in REQUIRED_KEYS:
        if key not in settings:
            logger.error(f"Key <<{key}>> is missing in settings.yaml")
            exit(1)

    return Config(
        accounts=get_accounts(),
        threads=settings.get("threads"),
        min_amount=settings.get("min_amount"),
        max_amount=settings.get("max_amount"),
        arb_rpc=settings.get("arb_rpc"),
        delay_before_start_min=settings.get("delay_before_start_min"),
        delay_before_start_max=settings.get("delay_before_start_max"),
    )
