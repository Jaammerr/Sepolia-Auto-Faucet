import random
import time
import requests

from hexbytes import HexBytes
from loguru import logger
from web3 import Web3, Account

from models import OnchainData
from loader import config

Account.enable_unaudited_hdwallet_features()


class SepoliaFaucet:
    def __init__(self, mnemonic_or_pk: str):
        self.w3 = Web3(Web3.HTTPProvider(config.arb_rpc))
        self.mnemonic_or_pk = mnemonic_or_pk
        self.wallet = (
            self.w3.eth.account.from_key(mnemonic_or_pk)
            if len(mnemonic_or_pk.split()) not in (12, 24)
            else self.w3.eth.account.from_mnemonic(mnemonic_or_pk)
        )

        self.bridge_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(OnchainData.bridge_contract),
            abi=OnchainData.bridge_abi,
        )

        self.uniswap_quoter = self.w3.eth.contract(
            address=Web3.to_checksum_address(OnchainData.uniswap_quoter),
            abi=OnchainData.uniswap_quoter_abi,
        )

    @staticmethod
    def get_amounts_to_bridge(amount_in: int) -> tuple[int, int]:
        amount_in_hex = Web3.to_hex(amount_in)[2:]
        if len(amount_in_hex) < 13:
            amount_in_hex = f"{'0' * (13 - len(amount_in_hex))}{amount_in_hex}"
        elif len(amount_in_hex) > 13:
            amount_in_hex = amount_in_hex[:13]

        json_data = [
            {
                "method": "eth_call",
                "params": [
                    {
                        "to": "0xb27308f9f90d607463bb33ea1bebb41c27ce5ab6",
                        "data": f"0xf7729d4300000000000000000000000082af49447d8a07e3bd95bd0d56f35241523fbab1000000000000000000000000e71bdfe1df69284f00ee185cf0d95d0c7680c0d40000000000000000000000000000000000000000000000000000000000000bb8000000000000000000000000000000000000000000000000000{amount_in_hex}0000000000000000000000000000000000000000000000000000000000000000",
                    },
                    "latest",
                ],
                "id": 82,
                "jsonrpc": "2.0",
            },
        ]
        response = requests.post("https://arb1.arbitrum.io/rpc", json=json_data)
        amount_out_hex = int(response.json()[0]["result"], 16)

        amount_out = float(amount_out_hex) * 0.95
        amount_out = Web3.to_wei(amount_out, "ether")
        if len(str(amount_out)) > 18:
            amount_out = int(amount_out / 1e18)

        return amount_in, amount_out

    def build_transaction(self, amount_to_bridge: int):
        amount_in, amount_out = self.get_amounts_to_bridge(amount_to_bridge)

        transaction = self.bridge_contract.functions.swapAndBridge(
            amount_in,
            amount_out,
            161,
            self.wallet.address,
            self.wallet.address,
            Web3.to_checksum_address("0x0000000000000000000000000000000000000000"),
            b"",
        )

        built_transaction = transaction.build_transaction(
            {
                "type": "0x2",
                "nonce": self.w3.eth.get_transaction_count(self.wallet.address),
                "maxFeePerGas": Web3.to_wei(0.01, "gwei"),
                "maxPriorityFeePerGas": Web3.to_wei(0.01, "gwei"),
                "value": amount_in + 5627000000000,
            }
        )

        return built_transaction

    def verify_balance(self) -> bool | float:
        amount_to_bridge: float = random.uniform(config.min_amount, config.max_amount)
        amount_to_bridge = Web3.to_wei(amount_to_bridge, "ether")

        balance = self.w3.eth.get_balance(self.wallet.address)

        if balance < amount_to_bridge:
            human_balance = self.w3.from_wei(balance, "ether")
            logger.error(
                f"Account: {self.wallet.address} | Insufficient balance: {human_balance} ETH\n"
            )
            return False

        return amount_to_bridge

    def wait_for_transaction(self, tx_hash: HexBytes) -> bool:
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)

        if receipt.status == 1:
            logger.success(
                f"Account: {self.wallet.address} | Transaction successful: {tx_hash.hex()}\n"
            )
            return True
        else:
            logger.error(
                f"Account: {self.wallet.address} | Transaction failed: {tx_hash.hex()}\n"
            )
            return False

    def send_transaction(self):
        try:
            amount_to_bridge = self.verify_balance()
            if not amount_to_bridge:
                return False, self.mnemonic_or_pk

            built_transaction = self.build_transaction(amount_to_bridge)
            signed = self.wallet.sign_transaction(built_transaction)
            tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)

            logger.info(
                f"Account: {self.wallet.address} | Sending transaction: {tx_hash.hex()}\n"
            )

            status = self.wait_for_transaction(tx_hash)
            if status:
                return True, self.mnemonic_or_pk
            else:
                return False, self.mnemonic_or_pk

        except Exception as error:
            if "max fee per gas less than block base fee:" in str(error):
                logger.error(
                    f"Account: {self.wallet.address} | Transaction failed due the block base fee | Retrying\n"
                )
                time.sleep(3)
                return self.send_transaction()

            logger.error(
                f"Account: {self.wallet.address} | Failed to send transaction: {error}\n"
            )
            return False, self.mnemonic_or_pk

    def process_random_delay(self):
        delay = random.randint(
            config.delay_before_start_min, config.delay_before_start_max
        )
        logger.info(
            f"Account: {self.wallet.address} | Waiting for {delay} seconds before start\n"
        )
        time.sleep(delay)

    def send_transaction_safe(self) -> tuple[bool, str]:
        try:
            self.process_random_delay()
            return self.send_transaction()

        except Exception as error:
            logger.error(
                f"Account: {self.wallet.address} | Unhandled error while sending transaction: {error}\n"
            )
            return False, self.mnemonic_or_pk
