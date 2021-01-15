from numix_imports import *

config = default.get('./config.json')


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config
        self.process = psutil.Process(os.getpid())
        print('"Info" cog loaded')

	
    @commands.command(aliases=["info", "dev", "stat", "stats"])
    async def about(self,ctx):
        ram = self.process.memory_full_info().rss / 1024**2
        embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
        embed.set_footer(text="Numix", icon_url=self.config.logo)
        embed.set_author(name="Numix Bot", icon_url=self.config.logo)
        embed.add_field(name="Developers:", value=f"{self.config.devs}", inline=False)
        embed.add_field(name="Bot Version:", value=f"{self.config.botversion}", inline=False)
        embed.add_field(name="Support Server:", value=f"{self.config.supportserver}", inline=False)
        embed.add_field(name="Invited Servers:", value=f"`{len(self.bot.guilds)}` Servers", inline=False)
        embed.add_field(name="All Members:", value=f"`{len(self.bot.users)}` Members", inline=False)
        embed.add_field(name="Loaded Commands:", value=len([x.name for x in self.bot.commands]), inline=False)
        embed.add_field(name="Ram Usage:", value=f"{ram} MB", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lookup(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        if user.activity is not None:
            game = user.activity.name
        else:
            game = None
        voice_state = None if not user.voice else user.voice.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
        embed.add_field(name='User:', value=f"{user.name}#{user.discriminator}(`{user.id}`)", inline=False)
        embed.add_field(name='Nick:', value=user.nick, inline=False)
        embed.add_field(name='Status:', value=user.status, inline=False)
        embed.add_field(name='On Mobile:', value=user.is_on_mobile(), inline=False)
        embed.add_field(name='In Voice:', value=voice_state, inline=False)
        embed.add_field(name='Game / Custom Status:', value=game, inline=False)
        embed.add_field(name='Highest Role:', value=user.top_role.name, inline=False)
        embed.add_field(name="Bot User:", value=f"{user.bot}", inline=False)
        embed.add_field(name='Account Created Date:', value=user.created_at.__format__('%A, %d. %B %Y'), inline=False)
        embed.add_field(name='Account Creation Time:', value=user.created_at.__format__('%H:%M:%S'), inline=False)
        embed.add_field(name='Join Date:', value=user.joined_at.__format__('%A, %d. %B %Y'), inline=False)
        embed.add_field(name='Joined Time:', value=user.joined_at.__format__('%H:%M:%S'), inline=False)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text='Numix', icon_url=self.config.logo)
        await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Info(bot))		
