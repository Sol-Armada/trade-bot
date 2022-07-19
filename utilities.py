from discord import Interaction

class Utilities():
    def get_values_from_modal(interaction: Interaction) -> dict:
        v = list(interaction.data.values())[1][0]["components"]
        i = {}
        for k in v:
            i[k["custom_id"]] = k["value"]
        return i
