from ast import Constant
from asyncio import constants
from code import interact
from dis import disco
import json
from typing import Container
from urllib import response

import discord
from discord.ext import commands
from constants import Constants
from objects.trade import Trade
from fuzzywuzzy import fuzz, process


# class LocationSearch(discord.ui.Modal):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)

#         self.add_item(discord.ui.InputText(label="Location"))

#     async def callback(self, interaction: discord.Interaction):
#         scores = []
#         for _, planet in enumerate(Constants.planets):
#             values = Constants.planets[planet]
#             ratios = [fuzz.ratio(str(self.children[0].value), str(value)) for value in values]
#             scores.append({ "name": planet, "score": max(ratios)})

#         filtered_scores = [item for item in scores if item["score"] >= 30]
#         sorted_scores = sorted(filtered_scores, key = lambda k: k['score'], reverse=True)
#         filtered_list = [ Constants.planets[item["name"]] for item in sorted_scores ]

#         if len(filtered_list) > 1:
#             view = discord.ui.View()

            
#             for f in filtered_list:
#                 b = discord.ui.Button(label=f[0])
#                 b.callback = self.test_callback
#                 b.custom_id = f[0]
#                 view.add_item(b)

#             b = discord.ui.Button(label="None")
#             b.callback = self.none_callback
#             view.add_item(b)

#             await interaction.response.send_message(view=view, ephemeral=True)
#         else:
#             await interaction.response.send_message(filtered_list[0])

#     async def test_callback(self, interaction: discord.Interaction):
#         selected = interaction.data.values()[0]
#         await interaction.response.send_message(f"You chose {selected}")

#     async def none_callback(self, interaction: discord.Interaction):
#         await interaction.response.send_message("Okay! I will cancel this entry.", ephemeral=True)

class LocationSelection(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose a location",
        min_values=1, max_values=1,
        options=Constants.outer_options
    )

    async def select_callback(self, select, interaction: discord.Interaction):
        # create the inner location selection object
        s = discord.ui.Select(placeholder="Choose an inner location", min_values=1, max_values=1)
        s.options = Constants.inner_options[select.values[0]]
        s.callback = self.inner_callback

        # create the view
        v = discord.ui.View()
        # add the object to the view
        v.add_item(s)

        #send it
        await interaction.response.send_message(view=v, ephemeral=True)

    async def inner_callback(self, interaction: discord.Interaction):
        selected = interaction.data['values'][0]
        await interaction.response.send_message(f"Buying from {selected}", ephemeral=True)

class TradeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Trade ledger and tracker"

    @commands.slash_command()
    async def buy(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=LocationSelection(), ephemeral=True)
        """
        choose buy location
        enter commodity
        enter purchased amount
        enter price
        """

        # trade = Trade()

    @commands.slash_command()
    async def sell(self, ctx: discord.ApplicationContext):
        """
        choose sell location
        enter sold amount
        enter sell price

        calculate profit
        save record to user file
        """


def setup(bot: commands.Bot):
    bot.add_cog(TradeCog(bot))




# class MyModal(discord.ui.Modal):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#
#         self.add_item(discord.ui.InputText(label="Short Input"))
#         self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))
#
#     async def callback(self, interaction: discord.Interaction):
#         embed = discord.Embed(title="Modal Results")
#         embed.add_field(name="Short Input", value=self.children[0].value)
#         embed.add_field(name="Long Input", value=self.children[1].value)
#         await interaction.response.send_message(embeds=[embed])


