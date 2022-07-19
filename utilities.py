from discord import Interaction
from fuzzywuzzy import fuzz, process


class Utilities():
    def get_values_from_modal(interaction: Interaction) -> dict:
        v = list(interaction.data.values())[1][0]["components"]
        i = {}
        for k in v:
            i[k["custom_id"]] = k["value"]
        return i

    def get_fuzzy(query: str, commodities: list):
        scores = [fuzz.ratio(query, value) for value in commodities]
        scores = list(zip(scores, commodities))
        
        filtered_scores = [item for item in scores if item[0] >= 51]
        sorted_scores = sorted(filtered_scores, key = lambda k: k[0], reverse=True)

        return sorted_scores
