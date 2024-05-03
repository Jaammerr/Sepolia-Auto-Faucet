import os
import sys

from concurrent.futures import Future

import urllib3
from loguru import logger
from art import tprint


def setup():
    urllib3.disable_warnings()
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<light-cyan>{time:HH:mm:ss}</light-cyan> | <level> {level: <8}</level> | - <white>{"
        "message}</white>",
    )
    logger.add("logs.log", rotation="1 day", retention="7 days")


def show_dev_info():
    tprint("JamBit")
    print("\033[36m" + "VERSION: " + "\033[34m" + "1.0" + "\033[34m")
    print("\033[36m" + "Channel: " + "\033[34m" + "https://t.me/JamBitPY" + "\033[34m")
    print(
        "\033[36m"
        + "GitHub: "
        + "\033[34m"
        + "https://github.com/Jaammerr"
        + "\033[34m"
    )
    print(
        "\033[36m"
        + "DONATION EVM ADDRESS: "
        + "\033[34m"
        + "0xe23380ae575D990BebB3b81DB2F90Ce7eDbB6dDa"
        + "\033[0m"
    )
    print()


def export_wallets(tasks: list[Future[tuple[bool, str]]]):
    config_path = os.path.join(os.getcwd(), "config")
    success_wallets = open(os.path.join(config_path, "success_wallets.txt"), "a")
    failed_wallets = open(os.path.join(config_path, "failed_wallets.txt"), "a")

    for task in tasks:
        wallet, result = task.result()
        if wallet:
            success_wallets.write(result + "\n")
        else:
            failed_wallets.write(result + "\n")

    success_wallets.close()
    failed_wallets.close()
    logger.debug(f"Exported {len(tasks)} wallets")
