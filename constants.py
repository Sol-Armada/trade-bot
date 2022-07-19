import discord
from enum import Enum


class Constants:
    outer_options = [
        discord.SelectOption(
            label="Rest Stop"
        ),
        discord.SelectOption(
            label="Planetary"
        )
    ]

    inner_options = {
        "Rest Stop": [
            discord.SelectOption(
                label="ARC-L1"
            ),
            discord.SelectOption(
                label="ARC-L2"
            ),
            discord.SelectOption(
                label="ARC-L3"
            ),
            discord.SelectOption(
                label="CRU-L1"
            ),
            discord.SelectOption(
                label="CRU-L2"
            ),
            discord.SelectOption(
                label="CRU-L3"
            )
        ],
        "Planetary": [
            discord.SelectOption(
                label="Crusader"
            ),
            discord.SelectOption(
                label="ArcCorp"
            ),
            discord.SelectOption(
                label="Hurston"
            ),
            discord.SelectOption(
                label="Microtech"
            )
        ]
    }

    class TradeStatus(Enum):
        PENDING = 0
        CANCELED = 1
        COMPLETE = 2

