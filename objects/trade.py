from dataclasses import dataclass
from snowflake import SnowflakeGenerator
from constants import Constants
gen = SnowflakeGenerator(1)


@dataclass
class Trade:
    commodity: str

    purchase_amount: int
    purchase_location: str
    purchase_unit_price: float

    sell_amount: int
    sell_location: str
    sell_price: float

    trader_id: int  # grab discord member.display_name upon lookup
    status: Constants.TradeStatus

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
