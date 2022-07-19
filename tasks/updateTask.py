import os
import requests
from discord.ext import tasks, commands
from github import Github


class UpdateTask(commands.Cog):
    repo = None
    def __init__(self) -> None:
        client = Github(os.environ("GITHUB_TOKEN"))
        self.repo = client.get_repo(os.environ("GITHUB_REPO"))

    def cog_unload(self) -> None:
        return super().cog_unload()

    def get_current_release(self) -> str:
        f = open("current_release.txt", "r")
        return f.readline()

    @tasks.loop(seconds=60)
    async def check(self):
        latest_release = self.repo.get_latest_release()
        if latest_release != self.get_current_release():
            # download the latest release
            resp = requests.get(latest_release.url)
            with open(os.environ("DOWNLOAD_LOC") + "/update.zip", 'wb') as f:
                f.write(resp.content)
