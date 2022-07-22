import os
import platform
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utilities import Log, LogLevel

load_dotenv()

intents = discord.Intents.default()
token = os.getenv("TOKEN")

# global constants
LOG_LEVEL = LogLevel.DEBUG if os.getenv(
    "DEBUG", "false").lower() in ('true', '1', 't') else LogLevel.INFO
CHECK_FOR_UPDATES = os.getenv(
    "CHECK_FOR_UPDATES", "false").lower() in ('true', '1', 't')
USE_SUPERVISOR = os.getenv(
    "USE_SUPERVISOR", "false").lower() in ('true', '1', 't')


class TradeBot(commands.Bot):
    def __init__(self):
        # setup the logger
        self.log = Log("main", LOG_LEVEL).get_logger()

        self.here = os.path.dirname(os.path.abspath(__file__))
        super(TradeBot, self).__init__(
            intents=intents
        )
        self.log.info(f"starting bot on python {platform.python_version()}")
        self.log.info(f"using discord.py {discord.__version__}")

        # load the cogs
        for filename in os.listdir(os.path.join(self.here, "cogs")):
            if filename.endswith("py"):
                self.load_extension(f"cogs.{filename[:-3]}")
                self.log.info(f"cog {filename} is loaded")

        # load the tasks
        for filename in os.listdir(os.path.join(self.here, "tasks")):
            if filename.endswith("py"):
                self.load_extension(f"tasks.{filename[:-3]}")
                self.log.info(f"task {filename} is loaded")

    def run(self):
        return super().run(token)

    async def on_ready(self):
        self.log.info(f"bot logged in as {self.user}")


if __name__ == "__main__":
    bot = TradeBot()
    bot.run()
