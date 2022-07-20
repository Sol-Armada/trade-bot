import json
import os
from platform import release
import shutil
import subprocess
import tarfile
import discord
import requests
from datetime import datetime
from os.path import exists
from discord.ext import tasks, commands
from dotenv import load_dotenv

from main import TradeBot

load_dotenv()


class UpdateTask(commands.Cog):
    download_loc = None
    def __init__(self):
        if os.getenv("CHECK_FOR_UPDATES", "false").lower() in ('true', '1', 't'):
            self.download_loc = os.getenv("DOWNLOAD_LOC", "/tmp/")
            self.client = requests.session()
            self.client.headers = {
                "Accept": "application/vnd.github+json",
                "User-Agent": "robo-request"
            }
            if not exists("./current_release.txt"):
                open("./current_release.txt", 'a').close()
            
            self.check.start()

    @tasks.loop(seconds=90)
    async def check(self):
        try:
            resp = self.client.get(f"https://api.github.com/repos/{os.getenv('GITHUB_REPO', 'sol-armada/discord-bot')}/releases")
            
            rate_limit = int(resp.headers.get("X-RateLimit-Remaining"))
            if rate_limit > 0 and resp.status_code == 200:
                    latest_release = resp.json()[0]
                    download_link = latest_release["tarball_url"]

                    if latest_release["id"] != self.get_current_release() and not bool(latest_release["draft"]):
                        resp = self.client.get(download_link)
                        with open(os.path.join(self.download_loc, "bot.tar.gz"), 'wb') as f:
                            f.write(resp.content)
                        self.save_current_release(latest_release["id"])
                        self.apply_release()
                        self.save_release_info(latest_release)
            else:
                reset_time = datetime.fromtimestamp(int(resp.headers.get("X-RateLimit-Reset")))
                time_left = reset_time - datetime.now()
                print(f"Github Rate Limited. Reset in {time_left.seconds} seconds")
        except Exception as e:
            print(e)

    @check.error
    async def check_error(seld, error):
        print(error)

    @commands.slash_command()
    async def version(self, ctx: discord.ApplicationContext):
        release_info = self.get_release_info()
        embed_version = discord.Embed(
            type="rich",
        )
        embed_version.add_field(name="Version", value=release_info["name"])
        embed_version.add_field(name="Link", value=release_info["link"])

        await ctx.respond(embed=embed_version)

    def get_release_info(self) -> dict:
        f = open("./release_info.txt", "r")
        return json.loads(f.read())

    def save_release_info(self, release_info):
        with open("./release_info.txt", "w") as f:
            f.write(json.dumps({
                "link": release_info["html_url"],
                "name": release_info["name"],
                "prelease": bool(release_info["prerelease"]),
                "published_at": release_info["published_at"]
            }))

    def get_current_release(self) -> str:
        f = open("./current_release.txt", "r")
        return int(f.readline())

    def save_current_release(self, id: int):
        f = open("./current_release.txt", "w")
        f.write(str(id))

    def apply_release(self):
        try:
            with tarfile.open(os.path.join(self.download_loc, "bot.tar.gz"), "r") as tf:
                folder_name = tf.next().name
                tf.extractall(path=self.download_loc)
                shutil.move(os.path.join(self.download_loc, folder_name), os.getcwd(), copy_function=shutil.copytree)

                tf.close()
            if os.getenv("SUPERVISOR", "false").lower()  in ('true', '1', 't'):
                subprocess.run(["supervisorctl", "restart", "all"])
        except Exception as e:
            print(e)

def setup(bot: commands.Bot):
    bot.add_cog(UpdateTask())
