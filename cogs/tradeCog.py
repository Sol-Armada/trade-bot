import discord
from discord.ext import commands
from constants import Constants
from objects.trade import Trade
from fuzzywuzzy import fuzz, process
from utilities import Utilities

# class LocationSearch(discord.ui.Modal):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)

#         self.add_item(discord.ui.InputText(label="Location"))

#     async def callback(self, interaction: discord.Interaction):
        # scores = []
        # for _, planet in enumerate(Constants.planets):
        #     values = Constants.planets[planet]
        #     ratios = [fuzz.ratio(str(self.children[0].value), str(value)) for value in values]
        #     scores.append({ "name": planet, "score": max(ratios)})

        # filtered_scores = [item for item in scores if item["score"] >= 30]
        # sorted_scores = sorted(filtered_scores, key = lambda k: k['score'], reverse=True)
        # filtered_list = [ Constants.planets[item["name"]] for item in sorted_scores ]

        # if len(filtered_list) > 1:
        #     view = discord.ui.View()

            
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

class CreateBuy(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose a location",
        min_values=1, max_values=1,
        options=[discord.SelectOption(label=name) for name in Constants.trade_options]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        # build the options list
        options = []
        for name in Constants.trade_options[select.values[0]]:
            options.append(discord.SelectOption(label=name))

        # create the inner location selection object
        selection_dropdown = discord.ui.Select(placeholder="Choose an inner location", min_values=1, max_values=1)
        selection_dropdown.options = options
        if isinstance(Constants.trade_options[select.values[0]], dict):
            selection_dropdown.callback = self.outpost_callback
        else:
            selection_dropdown.callback = self.trade_information_callback

        # create the view
        view = discord.ui.View()
        # add the object to the view
        view.add_item(selection_dropdown)

        #send it
        await interaction.response.send_message(view=view, ephemeral=True)

    async def outpost_callback(self, interaction: discord.Interaction):
        # get the previously selected value
        selected = interaction.data["values"][0]

        # build the options list
        options = []
        for name in Constants.trade_options["Planet/Moon Outpost"][selected]:
            options.append(discord.SelectOption(label=name))

        # create the outpost location selection object
        s = discord.ui.Select(placeholder="Choose an inner location", min_values=1, max_values=1)
        s.options = options
        s.callback = self.trade_information_callback

        # create the view
        view = discord.ui.View()
        # add the object to the view
        view.add_item(s)

        #send it
        await interaction.response.send_message(view=view, ephemeral=True)

    async def trade_information_callback(self, interaction: discord.Interaction):
        selected = interaction.data["values"][0]

        # create the modal
        m = discord.ui.Modal(title="Trade information")
        m.callback = self.cost_modal_callback

        # add them to the modal
        m.add_item(discord.ui.InputText(label="item", custom_id="item"))
        m.add_item(discord.ui.InputText(label="amount", custom_id="purchase_amount"))
        m.add_item(discord.ui.InputText(label="price", custom_id="purchase_price"))

        # send it
        await interaction.response.send_modal(modal=m)

    async def cost_modal_callback(self, interaction: discord.Interaction):
        info = Utilities.get_values_from_modal(interaction)

        filtered_list = Utilities.get_fuzzy(info["item"], list(Constants.items.keys()))
        if len(filtered_list) > 1:
            view = discord.ui.View()

            for f in filtered_list:
                b = discord.ui.Button(label=f[0])
                b.callback = self.test_callback
                b.custom_id = f[0]
                view.add_item(b)

            b = discord.ui.Button(label="None")
            b.callback = self.none_callback
            view.add_item(b)

            await interaction.response.send_message(view=view, ephemeral=True)
        else:
            await interaction.response.send_message(f"some data ", ephemeral=True)

class TradeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Trade ledger and tracker"

    @commands.slash_command()
    async def buy(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Buying")
        fields = [
            "Location",
            "Commodity",
            "Purchase Price",
            "Amount Purchased"
        ]
        for field in fields:
            embed.add_field(name=field, value="Not Entered")

        await ctx.respond(embed=embed, view=CreateBuy(), ephemeral=True)
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
