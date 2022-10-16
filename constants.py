import discord
from enum import Enum


class Constants:
    data_folder = "C:/Users/Ryan/PycharmProjects/discord-bot/data/Sol_Armada_Traders"

    trade_options = {
        "Planet/Moon Outpost": {
            "Aberdeen": [
                "HDMS-Anderson",
                "HDMS-Norgaard"
            ],
            "Arial": [
                "HDMS-Bezdek",
                "HDMS-Lathan"
            ],
            "Calliope": [
                "Rayari Anvik Research Outpost",
                "Rayari Kaltag Research Outpost",
                "Shubin Mining Facility SMCa-6",
                "Shubin Mining Facility SMCa-8"
            ],
            "Cellin": [
                "Gallete Farms",
                "Hickes Research",
                "Terra Mills Hydrofarm",
                "Tram & Myers",
                "Private Property"
            ],
            "Clio": [
                "Rayari Cantwell Research Outpost",
                "Rayari McGrath Research Outpost"
            ],
            "Daymar": [
                "ArcCorp Mining Area 141",
                "Bountiful Harvest Hydroponics",
                "Kudre Ore",
                "Shubin Mining Facility SCD-1",
                "Brio's Breaker Yard",
                "Nuen Waste Management"
            ],
            "Euterpe": [
                "Bud's Growery",
                "Devlin Scrap & Salvage"
            ],
            "Hurston": [
                "HDMS-Edmond",
                "HDMS-Hadley",
                "HDMS-Oparei",
                "HDMS-Pinewood",
                "HDMS-Stanhope",
                "HDMS-Thedus",
                "Reclamation & Disposal Orinth"
            ],
            "Ita": [
                "HDMS-Ryder",
                "HDMS-Woodruff"
            ],
            "Lyria": [
                "Humboldt Mines",
                "Loveridge Mineral Reserve",
                "Shubin Mining Facility SAL-2",
                "Shubin Mining Facility SAL-5",
                "The Orphanage"
            ],
            "Magda": [
                "HDMS-Hahn",
                "HDMS-Perlman"
            ],
            "Microtech": [
                "Rayari Deltana Research Outpost",
                "Shubin Mining Facility SM0-10",
                "Shubin Mining Facility SM0-13",
                "Shubin Mining Facility SM0-18",
                "Shubin Mining Facility SM0-22",
                "The Necropolis"
            ],
            "Wala": [
                "ArcCorp Mining Area 045",
                "ArcCorp Mining Area 048",
                "ArcCorp Mining Area 056",
                "ArcCorp Mining Area 061",
                "Samson & Son's Salvage Center",
                "Shady Glen Farms"
            ],
            "Yela": [
                "ArcCorp Mining Area 157",
                "Benson Mining Outpost",
                "Deakins Research"
            ]
        },
        "City": [
            "Area 18 TDD",
            "Area 18 IO North",
            "Lorville CBD",
            "Lorville L19 Residences Admin Office",
            "Orison TDD",
            "Orison Municipal Services",
            "New Babbage TDD",
            "New Babbage MT Planetary Services"
        ],
        "Rest Stop": [
            "ARC-L1 Wide Forest Station Admin",
            "ARC-L2 Lively Pathway Station Admin",
            "ARC-L3 Modern Express Station Admin",
            "ARC-L4 Faint Glen Station Admin",
            "ARC-L5 Yellow Core Station Admin",
            "CRU-L1 Ambitious Dream Station Admin",
            "CRU-L4 Shallow Fields Station Admin",
            "CRU-L5 Beautiful Glen Station Admin",
            "HUR-L1 Green Glade Station Admin",
            "HUR-L2 Faithful Dream Station Admin",
            "HUR-L3 Thundering Express Station Admin",
            "HUR-L4 Melodic Fields Station Admin",
            "HUR-L5 High Course Station Admin",
            "MIC-L1 Shallow Frontier Station Admin",
            "MIC-L2 Long Forest Station Admin",
            "MIC-L3 Endless Odyssey Station Admin",
            "MIC-L4 Red Crossroads Station Admin",
            "MIC-L5 Modern Icarus Station Admin"
        ],
        "Orbital Station / Grim HEX": [
            "Port Olisar",
            "Everus Harbor",
            "Port Tressler",
            "Baijini Point",
            "Grim HEX",
        ]
    }

    items = {
        "Agricium": {
            "SCU": 6,
        },
        "Agricultural Supplies": {
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
