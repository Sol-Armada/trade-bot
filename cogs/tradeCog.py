import json

import discord
import os
from discord.ext import commands
from constants import Constants
from models.player import Player
from utilities import Utilities
from models.trade import Trade
from datetime import datetime, timezone, timedelta
from models.player import Player

trades = {}


class LocationButtonSelect(discord.ui.View):
    def __init__(self, trader: Player):
        super().__init__()
        self.trader = trader
        self.trade = Trade()
        self.trade.trader_id = trader.discord_id
        recent_location = trader.most_recent_trade.purchase_location
        most_used_location = trader.most_used_location

        recent_location_button = discord.ui.Button(
            label=recent_location,
            custom_id=recent_location
        )
        recent_location_button.callback = self.button_callback
        self.add_item(recent_location_button)

        if trader.most_used_location != recent_location:
            most_used_location_button = discord.ui.Button(
                label=most_used_location,
                custom_id=most_used_location
            )
            most_used_location_button.callback = self.button_callback
            self.add_item(most_used_location_button)

        button_goto_dropdown = discord.ui.Button(label="Other Location...")
        button_goto_dropdown.callback = self.initiate_dropdown_from_button
        self.add_item(button_goto_dropdown)

    async def button_callback(self, interaction: discord.Interaction):
        trades[f"{interaction.user.id}-{interaction.message.id}"] = self.trade
        selected = interaction.data["custom_id"]
        self.trade.commodity = selected
        await trade_information_callback(interaction)

    async def initiate_dropdown_from_button(self, interaction: discord.Interaction):
        trades[f"{interaction.user.id}-{interaction.message.id}"] = self.trade
        await interaction.response.edit_message(view=LocationDropDownSelect())


class LocationDropDownSelect(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose trade location",
        min_values=1, max_values=1,
        options=[discord.SelectOption(label=name)
                 for name in Constants.trade_options]
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
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


class SellForm(discord.ui.Modal):
    def __init__(self, commodities_dict, user_id):
        super().__init__(title="Commodity Values (Selling)")
        self.commodities_dict = commodities_dict
        self.trader = Player(user_id)

        for commodity in commodities_dict:
            self.add_item(
                discord.ui.InputText(label=f"{commodity} Unit Price (sell)", custom_id=commodity)
            )

        self.callback = self.sell_form_callback

    async def sell_form_callback(self, interaction: discord.Interaction):
        item_values = Utilities.get_values_from_modal(interaction)
        profit = 0
        pending = self.trader.pending_trades

        for trade in pending:
            trade.sell_quantity = int(trade.purchase_quantity)
            trade.sell_price = float(item_values[trade.commodity].replace(',', ''))
            trade.mark_as_completed()

            profit += trade.calculated_profit

        final_message = "Trades marked as completed\n" + '\n'.join(str(trade) for trade in pending)

        await interaction.response.send_message(final_message)


async def trade_information_callback(interaction: discord.Interaction):
    trade = trades[f"{interaction.user.id}-{interaction.message.id}"]
    trade.created_at = f"{datetime.now(timezone.utc).isoformat()}"

    if 'values' in interaction.data:
        selected = interaction.data["values"][0]
    else:
        selected = interaction.data['custom_id']
    trade.purchase_location = selected

    # create the modal
    m = discord.ui.Modal(title="Trade information")
    m.callback = cost_modal_callback

    # add them to the modal
    m.add_item(discord.ui.InputText(
        label="item", custom_id="item"))
    m.add_item(discord.ui.InputText(
        label="quantity", custom_id="purchase_quantity"))
    m.add_item(discord.ui.InputText(
        label="price", custom_id="purchase_unit_price"))

    # send it
    await interaction.response.send_modal(modal=m)


async def cost_modal_callback(interaction: discord.Interaction):
    trade = trades[f"{interaction.user.id}-{interaction.message.id}"]
    item_amt_cost = Utilities.get_values_from_modal(interaction)

    # set the quantity and price to the trade
    trade.purchase_quantity = int(item_amt_cost['purchase_quantity'].replace(",", ""))
    trade.purchase_unit_price = float(item_amt_cost['purchase_unit_price'].replace(",", ""))

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


async def button_callback(interaction: discord.Interaction):
    trade = trades[f"{interaction.user.id}-{interaction.message.id}"]
    selected = interaction.data["custom_id"]
    trade.commodity = selected
    await final_callback(interaction)


async def final_callback(interaction: discord.Interaction):
    trade = trades[f"{interaction.user.id}-{interaction.message.id}"]

    # build the embed to show the user what they inputted
    embed = discord.Embed(title="Buying")
    embed.add_field(name="Location", value=trade.purchase_location)
    embed.add_field(name="Commodity", value=trade.commodity)
    embed.add_field(name="Purchase Price", value=trade.purchase_unit_price)
    embed.add_field(name="Amount Purchased", value=trade.purchase_quantity)

    await interaction.response.edit_message(embed=embed, view=None)

    # save the trade as it is
    trade.save()
    # remove it from the currently processing trades
    trades.pop(f"{interaction.user.id}-{interaction.message.id}")


class TradeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = "Trade ledger and tracker"

    @commands.slash_command(
        description="Input a purchase transaction"
    )
    async def buy(self, ctx: discord.ApplicationContext):
        trader = Player(ctx.author.id)
        resp = await ctx.send_response(
            content="Where are you buying from?",
            view=LocationButtonSelect(trader),
            ephemeral=True
        )

    @commands.slash_command(
        description="Input a sell transaction"
    )
    async def sell(self, ctx: discord.ApplicationContext):
        trader = Player(ctx.author.id)
        pending_trades = trader.pending_trades
        if not pending_trades:
            await ctx.respond("You have nothing to sell — we have no record of pending trades for you.")
            return

        commodity_sell_values = {
            pending.commodity: 0.00
            for pending in pending_trades
        }
        await ctx.interaction.response.send_modal(SellForm(commodity_sell_values, ctx.author.id))

    @commands.slash_command(
        description="Lost Cargo"
    )
    async def lost(self, ctx: discord.ApplicationContext):
        trader = Player(ctx.author.id)

        pending_trades = trader.pending_trades

        if not pending_trades:
            await ctx.respond("We have no record of pending trades for you.", ephemeral=True)
            return

        final_message = "Trades lost\n"
        for trade in pending_trades:
            trade.mark_as_lost()
            final_message += f"{trade}\n"

        await ctx.respond(final_message, ephemeral=True)

    @commands.slash_command(
        description="See the leaderboard for trades"
    )
    async def leaderboard(self, ctx: discord.ApplicationContext):
        traders = [
            Player(trader_id)
            for trader_id in os.listdir(Constants.data_folder)
        ]
        traders.sort(key=lambda player: player.total_earned, reverse=True)
        ids = [t.discord_id for t in traders]
        members = [await ctx.guild.fetch_member(ID) for ID in ids]

        embed = discord.Embed(title="Sol Armada Trade Leaderboard")

        leaderboard_text = ""
        for i, trader in enumerate(traders[:10]):
            member = members[i]
            member_handle = member.display_name
            if member_handle.startswith('['):
                member_handle = member.display_name.partition(']')[-1]

            leaderboard_text += f"{i + 1}) {member_handle}: {trader.total_earned} aUEC\n"
        embed.add_field(name="Top Ten Traders", value=leaderboard_text)

        trader_position = ''
        if str(ctx.author.id) in ids:
            trader_position_int = ids.index(str(ctx.author.id)) + 1
            if trader_position_int > 10:
                for i, member in enumerate(traders[trader_position_int - 2:trader_position_int + 1]):
                    member = members[i]
                    member_handle = member.display_name
                    if member_handle.startswith('['):
                        member_handle = member.display_name.partition(']')[-1]

                    trader_position += f"{trader_position_int - 1 + i}) {member_handle}: {member.total_earned} aUEC\n"
            else:
                trader_position = str(trader_position_int)
                embed.add_field(name="Your Position", value=trader_position, inline=False)
        else:
            trader_position = "No Record Found"
            embed.add_field(name="Your Position", value=trader_position, inline=False)

        await ctx.respond(embed=embed, view=None)

    @commands.slash_command(
        description="Shows Trader Information"
    )
    async def traderfile(self, ctx: discord.ApplicationContext, player: discord.Member = None):
        trader = Player(player.id if player is not None else ctx.author.id)

        name = player.display_name if player is not None else ctx.author.display_name
        name_possessive = name + "'"
        if not name.endswith('s'):
            name_possessive += "s"

        try:
            embed = discord.Embed(title=f"{name_possessive} Trader Profile")
            embed.add_field(
                name="Total Credits Earned",
                value=str(trader.total_earned),
                inline=False
            )
            embed.add_field(
                name="Previous Buy Location",
                value=trader.most_recent_trade.purchase_location,
                inline=False
            )
            embed.add_field(
                name="Most Used Buy Location",
                value=trader.most_used_location,
                inline=False
            )
            if pending := trader.pending_trades:
                embed.add_field(
                    name="Pending Trades",
                    value='\n'.join(str(trade) for trade in pending),
                    inline=False
                )
            await ctx.respond(embed=embed, ephemeral=True)
        except IndexError:
            await ctx.respond(f"No record for {name} exists.", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(TradeCog(bot))
