import os
import platform
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
token = os.getenv("TOKEN")


class TradeBot(commands.Bot):
    def __init__(self):
        self.config = None
        self.here = os.path.dirname(os.path.abspath(__file__))
        super(TradeBot, self).__init__(
            intents=intents
        )
        print(
            f"\n-> Starting Bot on Python {platform.python_version()}, "
            f"discord.py {discord.__version__}\n"
        )

        # load the cogs
        for filename in os.listdir(os.path.join(self.here, "cogs")):
            if filename.endswith("py"):
                self.load_extension(f"cogs.{filename[:-3]}")
                print(filename, "loaded.")

        # load the tasks
        for filename in os.listdir(os.path.join(self.here, "tasks")):
            if filename.endswith("py"):
                self.load_extension(f"tasks.{filename[:-3]}")
                print(filename, "loaded.")

    def run(self):
        return super().run(token)

    async def on_ready(self):
        print(f"We have logged in as {self.user}")

if __name__ == "__main__":
    bot = TradeBot()
    bot.run()
