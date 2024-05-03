from dataclasses import dataclass


@dataclass
class OnchainData:
    bridge_contract: str = "0xfcA99F4B5186D4bfBDbd2C542dcA2ecA4906BA45"
    bridge_abi: list = open("./abi/sepolia_abi.json", "r").read()

    uniswap_quoter: str = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
    uniswap_quoter_abi: list = open("./abi/geth_token_abi.json", "r").read()
