import os
import shutil
import tarfile
import requests
from datetime import datetime
from os.path import exists
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()

class UpdateTask(commands.Cog):
    def __init__(self):
        if os.environ["CHECK_FOR_UPDATES"] or False:
            self.client = requests.session()
            self.client.headers = {
                "Accept": "application/vnd.github+json"
            }
            if not exists("./current_release.txt"):
                open("./current_release.txt", 'a').close()
            self.check.start()

    @tasks.loop(seconds=90)
    async def check(self):
        resp = self.client.get(f"https://api.github.com/repos/{os.getenv('GITHUB_REPO') or 'sol-armada/discord-bot'}/releases")
        rate_limit = int(resp.headers.get("X-RateLimit-Remaining"))
        if rate_limit > 0:
            if resp.status_code == 200:
                latest_release = resp.json()[0]
                download_link = latest_release["tarball_url"]
                if latest_release["id"] != self.get_current_release():
                    # download the latest release
                    resp = self.client.get(download_link)
                    with open(f"{os.environ['DOWNLOAD_LOC']}/bot.tar.gz", 'wb') as f:
                        f.write(resp.content)
                    self.save_current_release(latest_release["id"])
                    self.apply_release()
        else:
            reset_time = datetime.fromtimestamp(int(resp.headers.get("X-RateLimit-Reset")))
            time_left = reset_time - datetime.now()
            print(f"Github Rate Limited. Reset in {time_left.seconds} seconds")

    def get_current_release(self) -> str:
        f = open("./current_release.txt", "r")
        return f.readline()

    def save_current_release(self, id: int):
        f = open("./current_release.txt", "w")
        f.write(str(id))

    def apply_release(self):
        with tarfile.open(f"{os.environ['DOWNLOAD_LOC']}/bot.tar.gz", "r") as tf:
            folder_name = tf.next().name
            tf.extractall(path=os.environ['DOWNLOAD_LOC'])
            shutil.move(os.path.join(os.environ['DOWNLOAD_LOC'], folder_name), "./")
            tf.close()

def setup(bot: commands.Bot):
    bot.add_cog(UpdateTask())
