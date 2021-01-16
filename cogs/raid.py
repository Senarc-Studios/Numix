from numix_imports import *

class Raid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")

    @command.Cog.listener()
    async def on_member_join(self, member):
        return

def setup(bot):
    bot.add_cog(Raid(bot))