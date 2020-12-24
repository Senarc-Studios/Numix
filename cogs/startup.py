from numix_imports import *

class StartUp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot has started.")

def setup(bot):
    bot.add_cog(StartUp(bot))