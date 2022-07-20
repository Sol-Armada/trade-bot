import os
from tabnanny import check
import requests
from discord.ext import tasks, commands
from github import Github
from dotenv import load_dotenv

load_dotenv()

class UpdateTask(commands.Cog):
    def __init__(self):
        try:
            repo_name = os.environ["GITHUB_REPO"]
            client = Github("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")
            self.repo = client.get_repo(full_name_or_id=repo_name)
            self.check.start()
        except Exception as e:
            print(e)

    @tasks.loop(seconds=5)
    async def check(self):
        test = self.repo.get_releases()
        # latest_release = self.repo.get_latest_release()
        # if latest_release != self.get_current_release():
        #     # download the latest release
        #     resp = requests.get(latest_release.url)
        #     with open(os.environ["DOWNLOAD_LOC"] + "/update.zip", 'wb') as f:
        #         f.write(resp.content)
        await check()

    @check.before_loop
    async def before_check(self):
        print("TEST 123456")

    @check.error
    async def check_error(self, error):
        print(error)

    def get_current_release(self) -> str:
        f = open("current_release.txt", "r")
        return f.readline()

def setup(bot: commands.Bot):
    print("setting up")
    t = bot.add_cog(UpdateTask())
    print(t)
