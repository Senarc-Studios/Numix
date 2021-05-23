
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

	@commands.command(cls=CustomCommand, description="Shows all of Numix's commands.")
	@commands.has_permissions(add_reactions=True,embed_links=True)
	async def help(self, ctx, command=None):
		cog = command
		"""Gets all cogs and commands of mine."""
		try:
			if cog is None:
				e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
				e.set_author(name="Numix Commands", icon_url=self.config.logo)
				e.add_field(name="•── Information:", value="\nYou can change the bot's prefix using `n!prefix set <prefix>`, and if you forget your prefix just ping the bot. You can see all the command help categories, to look at the commands, type `n!help <category>` and if you need help with a specific command you can type `n!help <command>`.", inline=False)
				e.add_field(name="•── Command Categories:", value="\n:arrow_right: `n!help general` - Shows all the general commands.\n\n:arrow_right: `n!help music` - Shows all the music commands.\n\n:arrow_right: `n!help fun` - Shows all the api and fun commands.\n\n:arrow_right: `n!help economy` - Shows all the commands related to the economy.\n\n:arrow_right: `n!help moderation` - Shows all the moderation commands.\n\n:arrow_right: `n!help admin` - Shows all the commands that are accessable to admins.", inline=False)
				e.set_footer(text="Numix", icon_url=self.config.logo)
				return await ctx.send(embed=e)
			else:
				found = False
				try:
					command_list = ""
					for c in self.bot.get_cog(cog).get_commands():
						if not c.hidden:
							command_list += f"`{c.name}` - **{c.description}**\n\n"
					halp=discord.Embed(timstamp=ctx.message.created_at, description=command_list, color=242424)
					halp.set_author(name=f"{cog} commands", icon_url=self.config.logo)
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
							e.set_author(name=f"{cog} command", icon_url=self.config.logo)
							e.add_field(name="Description", value=f"{c.description}", inline=False)
							e.add_field(name="Permissions", value=f"`{c.perms}`")
							e.add_field(name="Aliases", value=f"`{ali}`", inline=False)
							e.add_field(name="Usage", value=f"`{c.syntax}`")
							e.set_footer(text="Numix", icon_url=self.config.logo)
							await ctx.send(embed=e)
						else:
							e = discord.Embed(timestamp=ctx.message.created_at, description="It looks like you've found a invalid command/category. Did you make a typo?", color=0xFF0000)
							e.set_author(name="Numix Commands", icon_url=self.config.logo)
							e.set_footer(text="Numix", icon_url=self.config.logo)
							return await ctx.send(embed=e)
					except Exception as e:
						print(e)
						e = discord.Embed(timestamp=ctx.message.created_at, description="It looks like you've found a invalid command/category. Did you make a typo?", color=0xFF0000)
						e.set_author(name="Numix Commands", icon_url=self.config.logo)
						e.set_footer(text="Numix", icon_url=self.config.logo)
						return await ctx.send(embed=e)
		except Exception as e:
			print(e)

def setup(bot):
	bot.add_cog(Help(bot))