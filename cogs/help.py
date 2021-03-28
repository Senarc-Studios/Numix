from numix_imports import *

class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Help" cog loaded')

	@commands.command(aliases=["h", "elp"])
	async def help(self, ctx, *, command=None):
		if command is None:
			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name="Numix Commands", icon_url=self.config.logo)
			e.add_field(name="•── Information:", value="\nYou can change the bot's prefix using `n!prefix set <prefix>`, and if you forget your prefix just ping the bot. You can see all the command help categories, to look at the commands, type `n!help <category>` and if you need help with a specific command you can type `n!help <command>`.", inline=False)
			e.add_field(name="•── Command Categories:", value="\n:arrow_right: `n!help general` - Shows all the general commands.\n\n:arrow_right: `n!help music` - Shows all the music commands.\n\n:arrow_right: `n!help fun` - Shows all the api and fun commands.\n\n:arrow_right: `n!help economy` - Shows all the commands related to the economy.\n\n:arrow_right: `n!help moderation` - Shows all the moderation commands.\n\n:arrow_right: `n!help admin` - Shows all the commands that are accessable to admins.", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "general":
			e = discord.Embed(timestamp=ctx.message.created_at, description="`about` - Shows information about Numix.\n\n`avatar` - Shows the avatar of the user.\n\n`invite` - Gives all links related to Numix.\n\n`report` - Reports a member if reports are enabled in the server.\n\n`serverinfo` - Shows the general information about the server.", color=242424)
			e.set_author(name="Numix General Category", icon_url=self.config.logo)
			e.set_footer(text="Page 1/1", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "economy":
			e = discord.Embed(timestamp=ctx.message.created_at, description="`daily` - Get your daily salary.\n\n`monthly` - Get your monthly salary.\n\n`deposit` - Deposits a specified amount of money on your bank account.\n\n`withdraw` - Withdraws a specified amount of money on your bank account.\n\n`send-money` - Sends a specified amount of money to someone else's bank account.", color=242424)
			e.set_author(name="Numix Economy Category", icon_url=self.config.logo)
			e.set_footer(text="Page 1/1", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "moderation":
			e = discord.Embed(timestamp=ctx.message.created_at, description="`ban` - Bans a mentioned user with a reason.\n\n", color=242424)
			e.set_author(name="Numix Moderation Category", icon_url=self.config.logo)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "about":
			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name="Numix About Command", icon_url=self.config.logo)
			e.add_field(name="Required Permission", value="@everyone", inline=False)
			e.add_field(name="Command Aliases", value="`info`, `dev`, `stat`, `stats`, `ver`, and `version`", inline=False)
			e.add_field(name="Description", value="This command shows all the information about numix, and the stats.", inline=False)
			e.add_field(name="Usage", value="`n!about`  *No parameters available.*", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "avatar":
			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name="Numix Avatar Command", icon_url=self.config.logo)
			e.add_field(name="Required Permission", value="@everyone", inline=False)
			e.add_field(name="Command Aliases", value="`av`", inline=False)
			e.add_field(name="Description", value="This command shows yours or a mentioned user's avatar/profile picture.", inline=False)
			e.add_field(name="Usage", value="`n!avatar <user>`  *`<user>` parameter is optional.*", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "invite":
			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name="Numix Invite Command", icon_url=self.config.logo)
			e.add_field(name="Required Permission", value="@everyone", inline=False)
			e.add_field(name="Command Aliases", value="`inv`, `link`, `links`, `ss`, `support`, and `supportserver`", inline=False)
			e.add_field(name="Description", value="This command sends all the links and invites related to Numix.", inline=False)
			e.add_field(name="Usage", value="`n!invite`  *No parameters available.*", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "report":
			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name="Numix Report Command", icon_url=self.config.logo)
			e.add_field(name="Required Permission", value="@everyone", inline=False)
			e.add_field(name="Command Aliases", value="`N/A`", inline=False)
			e.add_field(name="Description", value="This command is used to report a user on the server if the reports system is enabled on the server.", inline=False)
			e.add_field(name="Usage", value="`n!report <user> <reason>`  *All parameters are required.*", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "serverinfo":
			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name="Numix ServerInfo Command", icon_url=self.config.logo)
			e.add_field(name="Required Permission", value="@everyone", inline=False)
			e.add_field(name="Command Aliases", value="`server`, and `server-info`", inline=False)
			e.add_field(name="Description", value="This command shows most of the information about the server.", inline=False)
			e.add_field(name="Usage", value="`n!serverinfo`  *No parameters available.*", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "lookup":
			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name="Numix Lookup Command", icon_url=self.config.logo)
			e.add_field(name="Required Permission", value="`MANAGE_MESSAGES`", inline=False)
			e.add_field(name="Command Aliases", value="`N/A`", inline=False)
			e.add_field(name="Description", value="This command shows information about the user.", inline=False)
			e.add_field(name="Usage", value="`n!lookup <user>`  *`<user>` parameter is optional.*", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		elif command == "daily":
			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name="Numix Daily Command", icon_url=self.config.logo)
			e.add_field(name="Required Permission", value="@everyone", inline=False)
			e.add_field(name="Command Aliases", value="`N/A`", inline=False)
			e.add_field(name="Description", value="This command gives you your daily salary.", inline=False)
			e.add_field(name="Usage", value="`n!daily`  *No parameters available.*", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

		else:
			e = discord.Embed(timestamp=ctx.message.created_at, description="It looks like you've found a invalid command/category. Did you make a typo?", color=0xFF0000)
			e.set_author(name="Numix Commands", icon_url=self.config.logo)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=e)

def setup(bot):
	bot.add_cog(Help(bot))