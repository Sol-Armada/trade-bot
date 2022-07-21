import discord
from discord.ext import commands
from constants import Constants
from utilities import Utilities
from objects.trade import Trade

class LocationTypeSelect(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose location type",
        min_values=1, max_values=1,
        options=[discord.SelectOption(label=name) for name in Constants.trade_options]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        trade = Trade()
        trade.trader_id = interaction.user.id

        chosen_location_type = select.values[0]
        if chosen_location_type == "Planet/Moon Outpost":
            await interaction.response.edit_message(
                view=MoonSelect(trade)
            )
        else:
            await interaction.response.edit_message(
                view=InnerSelect(chosen_location_type, trade)
            )


class InnerSelect(discord.ui.View):
    def __init__(self, selected_location, trade):
        super().__init__()
        inner_select_dropdown = discord.ui.Select(
            placeholder="Choose trade location",
            min_values=1, max_values=1,
            options=[
                discord.SelectOption(label=name)
                for name in Constants.trade_options[selected_location]
            ]
        )
        inner_select_dropdown.callback = trade_information_callback
        self.add_item(inner_select_dropdown)


class OutpostSelect(discord.ui.View):
    def __init__(self, outpost_names):
        super().__init__()
        inner_select_dropdown = discord.ui.Select(
            placeholder="Choose trade location",
            min_values=1, max_values=1,
            options=[
                discord.SelectOption(label=name)
                for name in outpost_names
            ]
        )
        inner_select_dropdown.callback = trade_information_callback
        self.add_item(inner_select_dropdown)


class MoonSelect(discord.ui.View):
    def __init__(self, trade):
        super().__init__()
        self.trade = trade
        inner_select_dropdown = discord.ui.Select(
            placeholder="Choose trade location",
            min_values=1, max_values=1,
            options=[
                discord.SelectOption(label=name)
                for name in Constants.trade_options["Planet/Moon Outpost"]
            ]
        )
        inner_select_dropdown.callback = self.outpost_callback
        self.add_item(inner_select_dropdown)

    async def outpost_callback(self, interaction):
        selected_moon = interaction.data['values'][0]
        await interaction.response.edit_message(
            view=OutpostSelect(
                Constants.trade_options["Planet/Moon Outpost"][selected_moon],
                self.trade
            )
        )


async def trade_information_callback(interaction: discord.Interaction):
    selected = interaction.data["values"][0]

    # create the modal
    m = discord.ui.Modal(title="Trade information")
    m.callback = cost_modal_callback

    # add them to the modal
    m.add_item(discord.ui.InputText(label="item", custom_id="item"))
    m.add_item(discord.ui.InputText(label="amount", custom_id="purchase_amount"))
    m.add_item(discord.ui.InputText(label="price", custom_id="purchase_price"))

    # send it
    await interaction.response.send_modal(modal=m)


async def button_callback(interaction: discord.Interaction):
    selected = interaction.data["custom_id"]
    await final_callback(interaction)


async def final_callback(interaction: discord.Interaction, trade):
    embed = discord.Embed(title="Buying")
    fields = [
        "Location",
        "Commodity",
        "Purchase Price",
        "Amount Purchased"
    ]
    for field in fields:
        embed.add_field(name=field, value="Not Entered")
    embed.fields[1].value = trade_data.get('')
    embed.fields[2].value = item_amt_cost.get('purchase_price')
    embed.fields[3].value = item_amt_cost.get('purchase_amount')
    await interaction.response.edit_message(embed=embed)


async def cost_modal_callback(interaction: discord.Interaction, trade):
    item_amt_cost = Utilities.get_values_from_modal(interaction)
    """
    {
        'item': '',
        'purchase_amount': '',
        'purchase_price': ''
    }
    """
    filtered_list = Utilities.get_fuzzy(item_amt_cost["item"], list(Constants.items.keys()))
    if len(filtered_list) > 1:
        view = discord.ui.View()

        for commodity in filtered_list[:5]:
            b = discord.ui.Button(label=commodity)
            b.callback = button_callback
            b.custom_id = commodity
            view.add_item(b)

        # b = discord.ui.Button(label="None")
        # b.callback = none_callback
        # view.add_item(b)

        await interaction.response.edit_message(view=view)
    else:
        item_amt_cost['item'] = filtered_list[0]
        await final_callback(interaction, trade)




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

        await ctx.respond(embed=embed, view=LocationTypeSelect(), ephemeral=True)

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
