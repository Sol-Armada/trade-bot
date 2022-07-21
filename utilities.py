from discord import Interaction
from fuzzywuzzy import fuzz, process


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
        scores = [fuzz.ratio(query.lower(), value.lower()) for value in items_to_search]
        scores = list(zip(scores, items_to_search))
        #  [(score, commodity), (score, commodity)]
        filtered_scores = [score for score in scores if score[0] >= 10]
        sorted_scores = sorted(filtered_scores, key=lambda k: k[0], reverse=True)
        if sorted_scores:
            first_score, first_item_name = sorted_scores[0]
            if first_score == 100:
                return [first_item_name]

        return [pair[1] for pair in sorted_scores]
