from dataclasses import dataclass


@dataclass
class Config:
    accounts: list[str]
    threads: int
    arb_rpc: str

    min_amount: float
    max_amount: float

    delay_before_start_min: int
    delay_before_start_max: int
