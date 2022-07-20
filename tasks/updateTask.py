import os
import shutil
import subprocess
import tarfile
import requests
from datetime import datetime
from os.path import exists
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()

class UpdateTask(commands.Cog):
    download_loc = None
    def __init__(self):
        if bool(os.getenv("CHECK_FOR_UPDATES")):
            self.download_loc = os.getenv("DOWNLOAD_LOC", "/tmp/")
            self.client = requests.session()
            self.client.headers = {
                "Accept": "application/vnd.github+json"
            }
            if not exists("./current_release.txt"):
                open("./current_release.txt", 'a').close()
            self.check.start()

    @tasks.loop(seconds=90)
    async def check(self):
        resp = self.client.get(f"https://api.github.com/repos/{os.getenv('GITHUB_REPO', 'sol-armada/discord-bot')}/releases")
        print(resp.request.headers)
        rate_limit = int(resp.headers.get("X-RateLimit-Remaining"))
        if rate_limit > 0 and resp.status_code == 200:
                latest_release = resp.json()[0]
                download_link = latest_release["tarball_url"]
                if latest_release["id"] != self.get_current_release():
                    # download the latest release
                    resp = self.client.get(download_link)
                    with open(f"{self.download_loc}/bot.tar.gz", 'wb') as f:
                        f.write(resp.content)
                    self.save_current_release(latest_release["id"])
                    self.apply_release()
        else:
            reset_time = datetime.fromtimestamp(int(resp.headers.get("X-RateLimit-Reset")))
            time_left = reset_time - datetime.now()
            print(f"Github Rate Limited. Reset in {time_left.seconds} seconds")

    @check.error
    async def check_error(seld, error):
        print(error)

    def get_current_release(self) -> str:
        f = open("./current_release.txt", "r")
        return f.readline()

    def save_current_release(self, id: int):
        f = open("./current_release.txt", "w")
        f.write(str(id))

    def apply_release(self):
        with tarfile.open(os.path(self.download_loc, "bot.tar.gz"), "r") as tf:
            folder_name = tf.next().name
            tf.extractall(path=self.download_loc)
            shutil.move(os.path.join(self.download_loc, folder_name), "./")
            tf.close()
        if bool(os.getenv("SUPERVISOR")):
            subprocess.run(["supervisorctl", "restart", "all"])

def setup(bot: commands.Bot):
    bot.add_cog(UpdateTask())
