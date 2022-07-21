from dataclasses import dataclass
from snowflake import SnowflakeGenerator
from constants import Constants
gen = SnowflakeGenerator(1)


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
    status: Constants.TradeStatus = Constants.TradeStatus.PENDING

    def __post_init__(self):
        self.receipt_id = next(gen)

    def mark_as_completed(self) -> None:
        self._set_status(Constants.TradeStatus.COMPLETE)

    def mark_as_canceled(self):
        self._set_status(Constants.TradeStatus.CANCELED)

    def _set_status(self, status: Constants.TradeStatus) -> None:
        self.status = status
        self.save()

    def save(self):
        ...

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
