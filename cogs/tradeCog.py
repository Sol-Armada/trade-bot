import discord
from discord.ext import commands
from constants import Constants
from utilities import Utilities
from objects.trade import Trade, save

trades = {}


class LocationTypeSelect(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose location type",
        min_values=1, max_values=1,
        options=[discord.SelectOption(label=name)
                 for name in Constants.trade_options]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        # make a new trade
        trade = Trade()
        trade.trader_id = interaction.user.id
        # apply it to the list of current trades
        trades[f"{interaction.message.id}_{interaction.user.id}"] = trade

        chosen_location_type = select.values[0]
        if chosen_location_type == "Planet/Moon Outpost":
            await interaction.response.edit_message(
                view=MoonSelect()
            )
        else:
            await interaction.response.edit_message(
                view=InnerSelect(chosen_location_type)
            )


class InnerSelect(discord.ui.View):
    def __init__(self, selected_location):
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


class MoonSelect(discord.ui.View):
    def __init__(self):
        super().__init__()
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
                Constants.trade_options["Planet/Moon Outpost"][selected_moon]
            )
        )


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


async def trade_information_callback(interaction: discord.Interaction):
    trade = trades[f"{interaction.message.id}_{interaction.user.id}"]
    selected = interaction.data["values"][0]
    trade.purchase_location = selected

    # create the modal
    m = discord.ui.Modal(title="Trade information")
    m.callback = cost_modal_callback

    # add them to the modal
    m.add_item(discord.ui.InputText(label="item", custom_id="item"))
    m.add_item(discord.ui.InputText(
        label="amount", custom_id="purchase_amount"))
    m.add_item(discord.ui.InputText(
        label="price", custom_id="purchase_unit_price"))

    # send it
    await interaction.response.send_modal(modal=m)


async def cost_modal_callback(interaction: discord.Interaction):
    trade = trades[f"{interaction.message.id}_{interaction.user.id}"]
    item_amt_cost = Utilities.get_values_from_modal(interaction)

    # set the amount and price to the trade
    trade.purchase_amount = int(item_amt_cost['purchase_amount'])
    trade.purchase_unit_price = float(item_amt_cost['purchase_unit_price'])

    # check if the commodity exists and get the closest
    filtered_list = Utilities.get_fuzzy(
        item_amt_cost["item"], list(Constants.items.keys()))
    if len(filtered_list) > 1:
        # found more than one possibility, ask which one they meant
        view = discord.ui.View()

        for commodity in filtered_list[:5]:
            b = discord.ui.Button(label=commodity)
            b.callback = button_callback
            b.custom_id = commodity
            view.add_item(b)

        await interaction.response.edit_message(view=view)
    else:
        trade.commodity = item_amt_cost['item']
        await final_callback(interaction)
    print(trade)


async def button_callback(interaction: discord.Interaction):
    trade = trades[f"{interaction.message.id}_{interaction.user.id}"]

    selected = interaction.data["custom_id"]
    trade.commodity = selected
    
    await final_callback(interaction)


async def final_callback(interaction: discord.Interaction):
    trade = trades[f"{interaction.message.id}_{interaction.user.id}"]

    # build the embed to show the user what they inputed
    embed = discord.Embed(title="Buying")
    embed.add_field(name="Location", value=trade.purchase_location)
    embed.add_field(name="Commodity", value=trade.commodity)
    embed.add_field(name="Purchase Price", value=trade.purchase_unit_price)
    embed.add_field(name="Amount Purchased", value=trade.purchase_amount)

    await interaction.response.edit_message(embed=embed, view=None)

    # save the trade as it is
    save(trade)
    # remove it from the currently processing trades
    trades.pop(f"{interaction.message.id}_{interaction.user.id}")


class TradeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Trade ledger and tracker"

    @commands.slash_command()
    async def buy(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=LocationTypeSelect(), ephemeral=True)

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
