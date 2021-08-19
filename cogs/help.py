
from numix_imports import *

class CustomCommand(commands.Command):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.perms = kwargs.get("perms", None)
        self.syntax = kwargs.get("syntax", None)

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Help" cog loaded')

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!help <command/category>", description="Shows all of Numix's commands.")
	@commands.has_permissions(embed_links=True)
	async def help(self, ctx, command=None):
		cog = command
		"""Gets all cogs and commands of mine."""
		try: 
			if cog is None:
				e = discord.Embed(timestamp=ctx.message.created_at, description=f"{self.config.ref_buttons}", color=242424)
				e.set_author(name="Numix Commands", icon_url=self.config.logo)
				e.add_field(name="•── Information:", value="\nYou can change the bot's prefix using `n!prefix set <prefix>`, and if you forget your prefix just ping the bot. You can see all the command help categories, to look at the commands, type *`n!help <category>`* and if you need help with a specific command you can type *`n!help <command>`*.", inline=False)
				e.add_field(name="•── Command Categories:", value=f"\n{self.config.arrow} `n!help general` - Shows all the general commands.\n\n{self.config.arrow} `n!help music` - Shows all the music commands.\n\n{self.config.arrow} `n!help fun` - Shows all the api and fun commands.\n\n{self.config.arrow} `n!help economy` - Shows all the commands related to the economy.\n\n{self.config.arrow} `n!help moderation` - Shows all the moderation commands.\n\n{self.config.arrow} `n!help admin` - Shows all the commands that are accessable to admins.", inline=False)
				e.set_footer(text="Numix", icon_url=self.config.logo)
				return await ctx.send(embed=e)
			else:
				found = False
				try:
					halp=discord.Embed(timstamp=ctx.message.created_at, color=242424)

					for c in self.bot.get_cog(cog).get_commands():
						if not c.hidden:
							halp.add_field(name=c.name, value=f"{self.config.arrow} {c.description}")
					
					halp.set_author(name=f"{cog.capitalize()} Commands", icon_url=self.config.logo)
					halp.set_footer(text="Numix", icon_url=self.config.logo)
					await ctx.send(embed=halp)
					found = True
				except Exception:
					found = False
				if not found:
					try:
						c = self.bot.get_command(cog)
						if not c.hidden:
							ali = f"{c.aliases}"
							if c.aliases == []:
								ali = "None"
							ali = ali.replace("[", "")
							ali = ali.replace("]", "")
							ali = ali.replace("'", "")
							ali = ali.replace('"', "")
							e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
							e.set_author(name=f"{cog.capitalize()} Command", icon_url=self.config.logo)
							e.add_field(name="Description", value=f"{self.config.arrow} {c.description}", inline=False)
							e.add_field(name="Permissions", value=f"{self.config.arrow} `{c.perms}`")
							e.add_field(name="Aliases", value=f"{self.config.arrow} `{ali}`", inline=False)
							e.add_field(name="Usage", value=f"{self.config.arrow} `{c.syntax}`")
							e.set_footer(text="Numix", icon_url=self.config.logo)
							await ctx.send(embed=e)
						else:
							e = discord.Embed(timestamp=ctx.message.created_at, description=f"{self.config.arrow} It looks like you've found a invalid command/category. Did you make a typo?", color=0xFF0000)
							e.set_author(name="Numix Commands", icon_url=self.config.logo)
							e.set_footer(text="Numix", icon_url=self.config.logo)
							return await ctx.send(embed=e)
					except Exception as e:
						print(e)
						e = discord.Embed(timestamp=ctx.message.created_at, description=f"{self.config.arrow} It looks like you've found a invalid command/category. Did you make a typo?", color=0xFF0000)
						e.set_author(name="Numix Commands", icon_url=self.config.logo)
						e.set_footer(text="Numix", icon_url=self.config.logo)
						return await ctx.send(embed=e)
		except Exception as e:
			print(e)

def setup(bot):
	bot.add_cog(Help(bot))