from concurrent.futures import ThreadPoolExecutor

from src.main import SepoliaFaucet
from src.util import export_wallets, show_dev_info, setup

from loader import config
from loguru import logger


def run():
    setup()
    show_dev_info()
    logger.info(
        f"\n\nBot Started | Threads: {config.threads} | Accounts: {len(config.accounts)}\n\n"
    )

    with ThreadPoolExecutor(max_workers=config.threads) as executor:
        tasks = [
            executor.submit(SepoliaFaucet(account.strip()).send_transaction_safe)
            for account in config.accounts
        ]

        export_wallets(tasks)


if __name__ == "__main__":
    run()
