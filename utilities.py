import logging
import sys
from enum import Enum
from discord import Interaction
from fuzzywuzzy import fuzz


class Utilities():
    @staticmethod
    def get_values_from_modal(interaction: Interaction) -> dict:
        v = list(interaction.data.values())[1]
        i = {}
        for k in v:
            c = k['components'][0]
            i[c.get('custom_id')] = c.get('value')
        return i

    @staticmethod
    def get_fuzzy(query: str, items_to_search: list):
        scores = [fuzz.ratio(query.lower(), value.lower())
                  for value in items_to_search]
        scores = list(zip(scores, items_to_search))
        #  [(score, commodity), (score, commodity)]
        filtered_scores = [score for score in scores if score[0] >= 10]
        sorted_scores = sorted(
            filtered_scores, key=lambda k: k[0], reverse=True)
        if sorted_scores:
            first_score, first_item_name = sorted_scores[0]
            if first_score == 100:
                return [first_item_name]

        return [pair[1] for pair in sorted_scores]


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
