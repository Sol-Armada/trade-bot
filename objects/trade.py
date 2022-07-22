import io
import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from snowflake import SnowflakeGenerator
from constants import Constants
gen = SnowflakeGenerator(1)


@dataclass_json
@dataclass
class Trade:
    commodity: str = ""
    purchase_amount: int = 0
    purchase_location: str = ""
    purchase_unit_price: float = 0

    sell_amount: int = 0
    sell_location: str = ""
    sell_price: float = 0

    trader_id: int = -1  # grab discord member.display_name upon lookup
    status: str = "pending"

    def __post_init__(self):
        self.receipt_id = next(gen)

    def mark_as_completed(self) -> None:
        self._set_status("complete")

    def mark_as_canceled(self):
        self._set_status("canceled")

    def _set_status(self, status: str) -> None:
        self.status = status
        self.save()

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)


def save(trade: Trade):
    print(trade.to_dict())
    with io.open(f'./data/{trade.trader_id}-{trade.receipt_id}', 'w') as f:
        f.write(json.dumps(trade.to_dict()))
