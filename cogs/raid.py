from numix_imports import *
import numix_raid as check

class Raid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")

    @commands.Cog.listener()
    @check.raid(5)
    async def on_member_join(self, member):
        return

def setup(bot):
    bot.add_cog(Raid(bot))