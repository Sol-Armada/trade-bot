import discord
from enum import Enum


class Constants:
    outer_options = [
        discord.SelectOption(
            label="Planet/Moon Outpost"
        ),
        discord.SelectOption(
            label="Trade Center (TDD, CBD)"
        ),
        discord.SelectOption(
            label="Rest Stop"
        ),
        discord.SelectOption(
            label="Orbital Station / Grim HEX"
        )
    ]

    inner_options = {
        "Planet/Moon Outpost": [
            discord.SelectOption(
                label="Aberdeen"
            ),
            discord.SelectOption(
                label="Arial"
            ),
            discord.SelectOption(
                label="Calliope"
            ),
            discord.SelectOption(
                label="Cellin"
            ),
            discord.SelectOption(
                label="Clio"
            ),
            discord.SelectOption(
                label="Daymar"
            ),
            discord.SelectOption(
                label="Euterpe"
            ),
            discord.SelectOption(
                label="Hurston"
            ),
            discord.SelectOption(
                label="Ita"
            ),
            discord.SelectOption(
                label="Lyria"
            ),
            discord.SelectOption(
                label="Magda"
            ),
            discord.SelectOption(
                label="Microtech"
            ),
            discord.SelectOption(
                label="Wala"
            ),
            discord.SelectOption(
                label="Yela"
            )
        ],
        "Major Trade Center (TDD, CBD)": [
            discord.SelectOption(
                label="Area 18 TDD"
            ),
            discord.SelectOption(
                label="Area 18 IO North"
            ),
            discord.SelectOption(
                label="Lorville CBD"
            ),
            discord.SelectOption(
                label="Lorville L19 Residences Admin Office"
            ),
            discord.SelectOption(
                label="Orison TDD"
            ),
            discord.SelectOption(
                label="Orison Municipal Services"
            ),
            discord.SelectOption(
                label="New Babbage TDD"
            ),
            discord.SelectOption(
                label="New Babbage MT Planetary Services"
            )
        ],
        "Rest Stop": [
            discord.SelectOption(
                label="ARC-L1 Wide Forest Station Admin"
            ),
            discord.SelectOption(
                label="ARC-L2 Lively Pathway Station Admin"
            ),
            discord.SelectOption(
                label="ARC-L3 Modern Express Station Admin"
            ),
            discord.SelectOption(
                label="ARC-L4 Faint Glen Station Admin"
            ),
            discord.SelectOption(
                label="ARC-L5 Yellow Core Station Admin"
            ),
            discord.SelectOption(
                label="CRU-L1 Ambitious Dream Station Admin"
            ),
            discord.SelectOption(
                label="CRU-L4 Shallow Fields Station Admin"
            ),
            discord.SelectOption(
                label="CRU-L5 Beautiful Glen Station Admin"
            ),
            discord.SelectOption(
                label="HUR-L1 Green Glade Station Admin"
            ),
            discord.SelectOption(
                label="HUR-L2 Faithful Dream Station Admin"
            ),
            discord.SelectOption(
                label="HUR-L3 Thundering Express Station Admin"
            ),
            discord.SelectOption(
                label="HUR-L4 Melodic Fields Station Admin"
            ),
            discord.SelectOption(
                label="HUR-L5 High Course Station Admin"
            ),
            discord.SelectOption(
                label="MIC-L1 Shallow Frontier Station Admin"
            ),
            discord.SelectOption(
                label="MIC-L2 Long Forest Station Admin"
            ),
            discord.SelectOption(
                label="MIC-L3 Endless Odyssey Station Admin"
            ),
            discord.SelectOption(
                label="MIC-L4 Red Crossroads Station Admin"
            ),
            discord.SelectOption(
                label="MIC-L5 Modern Icarus Station Admin"
            )
        ],
        "Orbital Station / Grim HEX": [
            discord.SelectOption(
                label="Port Olisar"
            ),
            discord.SelectOption(
                label="Everus Harbor"
            ),
            discord.SelectOption(
                label="Port Tressler"
            ),
            discord.SelectOption(
                label="Baijini Point"
            ),
            discord.SelectOption(
                label="Grim HEX"
            )
        ]
    }

    outpost_options = {
        "Aberdeen": [
            discord.SelectOption(
                label="HDMS-Anderson"
            ),
            discord.SelectOption(
                label="HDMS-Norgaard"
            )
        ],
        "Arial": [
            discord.SelectOption(
                label="HDMS-Bezdek"
            ),
            discord.SelectOption(
                label="HDMS-Lathan"
            )
        ],
        "Calliope": [
            discord.SelectOption(
                label="Rayari Anvik Research Outpost"
            ),
            discord.SelectOption(
                label="Rayari Kaltag Research Outpost"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SMCa-6"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SMCa-8"
            )
        ],
        "Cellin": [
            discord.SelectOption(
                label="Gallete Farms"
            ),
            discord.SelectOption(
                label="Hickes Research"
            ),
            discord.SelectOption(
                label="Terra Mills"
            ),
            discord.SelectOption(
                label="Tram & Myers"
            ),
            discord.SelectOption(
                label="Private Property"
            )
        ],
        "Clio": [
            discord.SelectOption(
                label="Rayari Cantwell Research Outpost"
            ),
            discord.SelectOption(
                label="Rayari McGrath Research Outpost"
            )
        ],
        "Daymar": [
            discord.SelectOption(
                label="ArcCorp Mining Area 141"
            ),
            discord.SelectOption(
                label="Bountiful Harvest Hydroponics"
            ),
            discord.SelectOption(
                label="Kudre Ore"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SCD-1"
            ),
            discord.SelectOption(
                label="Brio's Breaker Yard"
            ),
            discord.SelectOption(
                label="Nuen Waste Management"
            )
        ],
        "Euterpe": [
            discord.SelectOption(
                label="Bud's Growery"
            ),
            discord.SelectOption(
                label="Devlin Scrap & Salvage"
            )
        ],
        "Hurston": [
            discord.SelectOption(
                label="HDMS-Edmond"
            ),
            discord.SelectOption(
                label="HDMS-Hadley"
            ),
            discord.SelectOption(
                label="HDMS-Oparei"
            ),
            discord.SelectOption(
                label="HDMS-Pinewood"
            ),
            discord.SelectOption(
                label="HDMS-Stanhope"
            ),
            discord.SelectOption(
                label="HDMS-Thedus"
            ),
            discord.SelectOption(
                label="Reclamation & Disposal Orinth"
            )
        ],
        "Ita": [
            discord.SelectOption(
                label="HDMS-Ryder"
            ),
            discord.SelectOption(
                label="HDMS-Woodruff"
            )
        ],
        "Lyria": [
            discord.SelectOption(
                label="Humboldt Mines"
            ),
            discord.SelectOption(
                label="Loveridge Mineral Reserve"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SAL-2"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SAL-5"
            ),
            discord.SelectOption(
                label="The Orphanage"
            )
        ],
        "Magda": [
            discord.SelectOption(
                label="HDMS-Hahn"
            ),
            discord.SelectOption(
                label="HDMS-Perlman"
            )
        ],
        "Microtech": [
            discord.SelectOption(
                label="Rayari Deltana Research Outpost"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SM0-10"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SM0-13"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SM0-18"
            ),
            discord.SelectOption(
                label="Shubin Mining Facility SM0-22"
            ),
            discord.SelectOption(
                label="The Necropolis"
            )
        ],
        "Wala": [
            discord.SelectOption(
                label="ArcCorp Mining Area 045"
            ),
            discord.SelectOption(
                label="ArcCorp Mining Area 048"
            ),
            discord.SelectOption(
                label="ArcCorp Mining Area 056"
            ),
            discord.SelectOption(
                label="ArcCorp Mining Area 061"
            ),
            discord.SelectOption(
                label="Samson & Son's Salvage Center"
            ),
            discord.SelectOption(
                label="Shady Glen Farms"
            )
        ],
        "Yela": [
            discord.SelectOption(
                label="ArcCorp Mining Area 157"
            ),
            discord.SelectOption(
                label="Benson Mining Outpost"
            ),
            discord.SelectOption(
                label="Deakins Research"
            )
        ]
    }

    planetary_options = {
        "Crusader": [
            discord.SelectOption(
                label="Orison Admin"
            )
        ],
        "Hurston": [
            discord.SelectOption(
                label="Lorville Admin"
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

