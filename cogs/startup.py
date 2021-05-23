from numix_imports import *
from discordpy_slash import slash

class StartUp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('"StartUp" cog loaded')

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot has started.")
        await slash.sync_all_commands(self.bot, loading_message="We're proccessing your commmand currently.", hidden_commands=["e", "apply", "load", "unload", "reload", "restart", "run_ads"])

def setup(bot):
    bot.add_cog(StartUp(bot))