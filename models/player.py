import datetime
import json
import os

from constants import Constants
from models.trade import Trade
from statistics import mode

data_folder = os.getenv("DATA_FOLDER")

def complete_trades(sell_prices, pending_trades: list):
    for trade in pending_trades:
        trade.sell_quantity = trade.purchase_quantity
        trade.sell_price = sell_prices[trade.commodity]
        trade.mark_as_completed()


class Player:
    def __init__(self, discord_id):
        self.discord_id = discord_id

    @property
    def trade_history(self) -> list[Trade]:
        loaded_trades = []
        trader_directory = f'{data_folder}/{self.discord_id}'
        if not os.path.exists(trader_directory):
            os.mkdir(trader_directory)

        for filename in os.listdir(trader_directory):
            with open(f"{trader_directory}/{filename}", 'r') as trade_file:
                trade_data = Trade.from_json(trade_file.read())
                trade_data.receipt_id = filename.split('-')[1]
                loaded_trades.append(trade_data)

        return loaded_trades

    @property
    def pending_trades(self) -> list[Trade]:
        trades = list(filter(lambda trade: trade.status == "pending", self.trade_history))
        trades.sort(key=lambda trade: datetime.datetime.fromisoformat(trade.created_at))
        return trades

    #     self._inventory = {
    #         commodity: 0
    #         for commodity in Constants.items
    #     }
    #
    # @property
    # def inventory(self):
    #     return {
    #         commodity: quantity
    #         for commodity, quantity in self._inventory.items() if quantity > 0
    #     }

    @property
    def total_earned(self) -> int:
        return sum(
            trade.calculated_profit
            for trade in self.trade_history if trade.status == "completed"
        )

    @property
    def trade_locations(self) -> list[str]:
        return [t.purchase_location for t in self.trade_history]

    @property
    def most_used_location(self):
        return mode(self.trade_locations)

    @property
    def most_recent_trade(self) -> Trade | None:
        trades = self.trade_history
        if not trades:
            return None
        trades.sort(key=lambda t: datetime.datetime.fromisoformat(t.created_at))
        return trades[-1]

    @property
    def oldest_pending_trade(self) -> Trade | None:
        trades = self.pending_trades
        return trades[0] if trades else None


if __name__ == "__main__":
    pass

    # for trade in trader.trade_history:
    #     print(json.dumps(trade.__dict__, indent=2), end="\n————————————————\n")
    #     print(trade)

