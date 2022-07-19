import json

import discord
from discord.ext import commands
from constants import Constants
from objects.trade import Trade


class LocationSelection(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose a location",
        min_values=1, max_values=1,
        options=Constants.outer_options
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        s = discord.ui.Select(
            placeholder="Choose a location",
            min_values=1, max_values=1,
            options=Constants.inner_options[select.values[0]]
        )
        await interaction.response.send_message(view=discord.ui.View(s), ephemeral=True)

    # class InnerLocationSelection(discord.ui.Select):
    #     @discord.ui.select(
    #         placeholder="Choose a location",
    #         min_values=1, max_values=1,
    #         options=Constants.inner_options
    #     )
    #     async def select_callback(self, select, interaction: discord.Interaction):
    #         await interaction.response.send_message(
    #             f"Buying from {select.values[0]}",
    #             ephemeral=True
    #         )



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


