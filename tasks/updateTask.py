import os
import tarfile
import requests
from os.path import exists
from tabnanny import check
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()

class UpdateTask(commands.Cog):
    def __init__(self):
        self.client = requests.session()
        self.client.headers = {
            "Accept": "application/vnd.github+json"
        }
        if not exists("./current_release.txt"):
            open("./current_release.txt", 'a').close()
        self.check.start()

    @tasks.loop(seconds=5)
    async def check(self):
        resp = self.client.get(f"https://api.github.com/repos/{os.getenv('GITHUB_REPO') or 'sol-armada/discord-bot'}/releases")
        latest_release = dict(resp.json()[0])
        download_link = str(latest_release.tarball_url)
        if latest_release.id != self.get_current_release():
            # download the latest release
            resp = self.client.get(download_link)
            with open(f"{os.environ['DOWNLOAD_LOC']}/bot.tar.gz", 'wb') as f:
                f.write(resp.content)
            self.save_current_release(latest_release.id)
        await check()

    @check.before_loop
    async def before_check(self):
        print("TEST 123456")

    @check.error
    async def check_error(self, error):
        print(error)

    def get_current_release(self) -> str:
        f = open("./current_release.txt", "r")
        return f.readline()

    def save_current_release(self, id: int):
        f = open("./current_release.txt", "w")
        f.write(id).close()

    def apply_release():
        with tarfile.open(f"{os.environ['DOWNLOAD_LOC']}/bot.tar.gz", "r") as tf:
            tf.extractall(path="./extracted/").close()

def setup(bot: commands.Bot):
    t = bot.add_cog(UpdateTask())
    print(t)
