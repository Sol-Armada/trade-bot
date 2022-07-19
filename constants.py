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

    planets = {
        "Microtech": [
            "test_123"
        ],
        "ArcCorp": [
            "test_789"
            ],
        "Hurston": [
            "test_012"
            ],
        "Crusader": [
            "test_456"
        ],
    }

    rest_stops = {
        "ARC": {
            "L1",
            "L2",
            "L3"
        },
        "CRU": {
            "L1",
            "L2",
            "L3"
        },
    }

    items = {
        "Agricium": {
            "SCU": 6,
        },
        "Agricultrual Supplies": {
            "SCU": 0.01,
        },
        "Altruciatoxin": {
            "SCU": 0.01,
        },
        "Aluminum": {
            "SCU": 1,
        },
        "Amioshi Plague": {
            "SCU": 0.0012,
        },
        "Aphorite": {
            "SCU": 0.001,
        },
        "Astatine": {
            "SCU": 0.06,
        },
        "Beryl": {
            "SCU": 0.06,
        },
        "Bexalite": {
            "SCU": 1,
        },
        "Borase": {
            "SCU": 0.01,
        },
        "Chlorine": {
            "SCU": 0.06,
        },
        "Copper": {
            "SCU": 0.01,
        },
        "Corundum": {
            "SCU": 0.06,
        },
        "Degnous Root": {
            "SCU": 0.00108,
        },
        "Diamond": {
            "SCU": 0.06,
        },
        "Distilled Spirits": {
            "SCU": 0.01,
        },
        "Dolivine": {
            "SCU": 0.001,
        },
        "E'tam": {
            "SCU": 0.01,
        },
        "Fluorine": {
            "SCU": 0.06,
        },
        "Gold": {
            "SCU": 0.06,
        },
        "Golden Medmon": {
            "SCU": 0,
        },
        "Hadanite": {
            "SCU": 0.001,
        },
        "Heart of the Woods": {
            "SCU": 0.001,
        },
        "Hephaestanite": {
            "SCU": 0.01,
        },
        "Hydrogen": {
            "SCU": 0.06,
        },
        "Inert Materials": {
            "SCU": 0,
        },
        "Iodine": {
            "SCU": 0.06,
        },
        "Laranite": {
            "SCU": 0.06,
        },
        "Maze": {
            "SCU": 0.01,
        },
        "Medical Supplies": {
            "SCU": 0.06,
        },
        "Neon": {
            "SCU": 0.01,
        },
        "Pitambu": {
            "SCU": 0.00073,
        },
        "Processed Food": {
            "SCU": 0.01,
        },
        "Prota": {
            "SCU": 0.0006,
        },
        "Quantainium": {
            "SCU": 0,
        },
        "Quartz": {
            "SCU": 0.06,
        },
        "Ranta Dung": {
            "SCU": 0.0007,
        },
        "Red Festival Envelope": {
            "SCU": 0,
        },
        "Revenant Pod": {
            "SCU": 0.0001,
        },
        "Revenant Tree Pollen": {
            "SCU": 0.01,
        },
        "SLAM": {
            "SCU": 0.01,
        },
        "Scrap": {
            "SCU": 0.01,
        },
        "Stims": {
            "SCU": 0.01,
        },
        "Sunset Berries": {
            "SCU": 0,
        },
        "Taranite": {
            "SCU": 0.01,
        },
        "Titanium": {
            "SCU": 0.06,
        },
        "Tungsten": {
            "SCU": 0.06,
        },
        "Waste": {
            "SCU": 0.01,
        },
        "WiDoW": {
            "SCU": 0.01,
        },
    }

    class TradeStatus(Enum):
        PENDING = 0
        CANCELED = 1
        COMPLETE = 2

