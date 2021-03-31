from numix_imports import *

class April(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")

    def random_trigger():
        chances = [True, False, False, False, False]
        return random.choice(chances)

    @commands.Cog.listener()
    @commands.check(random_trigger)
    async def on_command(self, ctx):
        embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
        embed.set_author("Reward!", icon_url=self.config.logo)
        embed.add_field(name="You got a reward!", value="Since you've been using Numix for a while, you can redeem the premium version for free! We're giving this away to users who are using numix often, or new to Numix.", inline=False)
        embed.add_field(name="How to claim reward?", value="You just need to go in https://numix.xyz/premiumreward-6879 and login with your discord account to claim the reward.", inline=False)
        embed.set_footer(text="Numix", icon_url=self.config.logo)
        ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(April(bot))