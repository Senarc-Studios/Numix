from numix_imports import *

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")
        print('"Help" cog loaded')

    @commands.command(aliases=["h", "elp"])
    async def help(self, ctx, *, category=None):
        if category is None:
            embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
            embed.set_author(name="Numix Commands", icon_url=self.config.logo)
            embed.add_field(name="General", value="``` invite, info, avatar, server ```")
            embed.add_field(name="Fun", value="``` 8ball,  ```")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))