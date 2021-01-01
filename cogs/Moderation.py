from numix_imports import *

class Moderation(commands.Cog, name='Moderation'):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.s = self.config.success
		print('"Moderation" cog loaded')

	@commands.command()
	async def warn(self, ctx, user: discord.Member=None, *, reason=None):
		cluster = MongoClient('mongodb+srv://Benitz:6vsdPiReMc2nTukr@numix.dksdu.mongodb.net/Moderation?retryWrites=true&w=majority')
		collection = cluster.Moderation.warns
		
		if reason is None:
			await ctx.send(":no_entry_sign: You have to provide a reason.")

		else:
			try:
				embed = discord.Embed(timestamp=ctx.message.created_at, title=f"[Warned] {ctx.guild.name}", description=f"**Type:** Warn\n**Reason:**{reason}", color=0xFC6700)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await user.send(embed=embed)
				warn = {"_id":user.id, f"{ctx.guild.id}":{f"{ctx.message.id}":reason}}
				collection.insert_one(warn)
				await ctx.send(f"{self.s} {user.name}#{user.discriminator} warned *User was notified*")
			except discord.Forbidden:
				warn = {"_id":user.id, f"{ctx.guild.id}":{f"{ctx.message.id}":reason}}
				collection.insert_one(warn)
				await ctx.send(f"{self.s} {user.name}#{user.discriminator} warned *User was not notified*")

	@commands.command()
	async def infractions(self, ctx, user: discord.Member=None):
		cluster = MongoClient('mongodb+srv://Benitz:6vsdPiReMc2nTukr@numix.dksdu.mongodb.net/Moderation?retryWrites=true&w=majority')
		collection = cluster.Moderation.warns

		if user is None:
			await ctx.send(":no_entry_sign: Specify a user.")
	
		else:
			arguments = query[user.id][ctx.guild.id]
			finder = collection.find(arguments)
			for result in finder:
				infractions = result

			await ctx.send(f"{infractions}")


def setup(bot):
	bot.add_cog(Moderation(bot))
