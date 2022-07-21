import logging
import sys
from enum import Enum
from discord import Interaction
from fuzzywuzzy import fuzz


class Utilities():
    @staticmethod
    def get_values_from_modal(interaction: Interaction) -> dict:
        v = list(interaction.data.values())[1][0]["components"]
        i = {}
        for k in v:
            i[k["custom_id"]] = k["value"]
        return i

    @staticmethod
    def get_fuzzy(query: str, commodities: list):
        scores = [fuzz.ratio(query, value) for value in commodities]
        scores = list(zip(scores, commodities))

        filtered_scores = [item for item in scores if item[0] >= 51]
        sorted_scores = sorted(
            filtered_scores, key=lambda k: k[0], reverse=True)

        return sorted_scores


class LogLevel(Enum):
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class Log():
    def __init__(self, name: str, level: LogLevel = logging.INFO,
                 log_to_file: bool = False, filename: str = None):
        self.log = logging.getLogger(name)
        self.log.setLevel(level)

        handler = logging.FileHandler(
            filename=filename) if log_to_file else logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )

        handler.setFormatter(formatter)

        self.log.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        return self.log

    def info(self, message: str):
        self.log.info(message)

    def debug(self, message: str):
        self.log.debug(message)

    def error(self, message: str, err: Exception):
        self.log.error(message)
        self.log.error(err)
