from datetime import datetime, timezone
import io
import json
import os.path
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from snowflake import SnowflakeGenerator
from constants import Constants
import discord
gen = SnowflakeGenerator(1)
data_folder = os.getenv("DATA_FOLDER")


@dataclass_json
@dataclass
class Trade:
    commodity: str = ""
    purchase_quantity: int = 0
    purchase_location: str = ""
    purchase_unit_price: float = 0

    sell_quantity: int = 0
    sell_location: str = ""
    sell_price: float = 0

    trader_id: int = -1  # grab discord member.display_name upon lookup
    status: str = "pending"
    created_at: str = ""
    closed_at: str = ""

    def __post_init__(self):
        self.receipt_id = next(gen)

    def mark_as_completed(self) -> None:
        # TODO: capture sell location
        self.sell_location = "SELL LOCATION NOT CAPTURED"
        self._set_status("completed")

    def mark_as_canceled(self):
        self._set_status("canceled")

    def mark_as_lost(self):
        self.sell_quantity = -self.purchase_quantity
        self.sell_price = -self.purchase_unit_price
        self._set_status("lost")

    def _set_status(self, status: str) -> None:
        self.status = status
        self.closed_at = datetime.now(timezone.utc).isoformat()
        self.save()

    @property
    def calculated_profit(self):
        if self.sell_quantity == 0:
            return 0
        return int((self.sell_quantity * self.sell_price) - (self.purchase_quantity * self.purchase_unit_price))

    def __str__(self):
        match self.status:
            case "pending":
                return f"{self.purchase_quantity} units of {self.commodity}"
            case "completed":
                return f"{self.sell_quantity} units of {self.commodity}, gained **{self.calculated_profit:,} aUEC**"
            case "lost":
                return f"{self.purchase_quantity} units of {self.commodity}, lost {int(self.purchase_quantity * self.purchase_unit_price):,} aUEC"
            case "canceled":
                return f"{self.purchase_quantity} units of {self.commodity}".ljust(40) + "| **CANCELED**"

    def save(self):
        trader_directory = f'{data_folder}/{self.trader_id}'
        if not os.path.exists(trader_directory):
            os.mkdir(f'{trader_directory}')
        with io.open(f'{trader_directory}/{self.trader_id}-{self.receipt_id}', 'w') as f:
            f.write(json.dumps(self.to_dict(), indent=2))
