import discord 
from discord.ext import commands
import requests
from utils import default

class server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")

    @commands.command()
    async def serverinfo(self, ctx):
        e = sum([1 for m in ctx.guild.members if m.bot])
        humans = sum(not member.bot for member in ctx.guild.members)
        embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
        embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
        embed.add_field(name="Total Members:", value=f"{ctx.guild.member_count}", inline=False)
        embed.add_field(name="Bots:", value=f"{e}", inline=False)
        embed.add_field(name="Humans:", value=f"{humans}", inline=False)
        embed.add_field(name="Boosts:", value=f"{(ctx.guild.premium_subscription_count)}", inline=False)
        embed.set_footer(text="Numix", icon_url=self.config.logo)
        await ctx.send(embed=embed)


class Dog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('"Test Cat" cog loaded')

    @commands.command(description="Sends a random cat image")
    async def testcat(self, ctx):
        URL = f'https://api.thecatapi.com/v1/images/search'

        def check_valid_status_code(request):
            if request.status_code == 200:
                return request.json()

            return False

        def get_cat():
            request = requests.get(URL)
            data = check_valid_status_code(request)

            return data

        cat = get_cat()
        if not cat:
            await ctx.channel.send(
                "Couldn't get cat from API. Try again later.")

        else:
            #print(cat)
            cat = cat[0]['url']
            #agee = str(cat['url'])
            embed = discord.Embed(title='Catto', color=0xff0)
            embed.set_image(url=f"{cat}")
            await ctx.send(embed=embed)
            #await ctx.send(cat[0]['url'])

def setup(bot):
    bot.add_cog(Dog(bot))
