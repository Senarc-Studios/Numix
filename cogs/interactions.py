from numix_imports import *

class Interactions(commands.Cog):
	def __init__(self, bot):
		print("\"Interactions\" cog loaded")
		self.bot = bot
		self.config = default.get("./config.json")
		self.MONGO_CONNECTION = MongoClient(f"{self.config.db1}")
		self.MONGO = self.MONGO_CONNECTION.DataBase_1.interactions

	@commands.Cog.listener()
	async def on_command(self, ctx):
		if self.MONGO.count_documents({ "_id": ctx.command.name }) == 0:
			return self.MONGO.insert_one({ "_id": ctx.command.name, "uses": 1 })

		else:
			for data in self.MONGO.find({ "_id": ctx.command.name }):
				self.MONGO.update_one({ "_id": ctx.command.name }, { "$set": { "_id": ctx.command.name, "uses": data["uses"] + 1 } })
			
				for fdata in self.MONGO.find({ "_id": "all" }):
					self.MONGO.update_one({ "_id": "all" }, { "$set": { "_id": "all", "uses": fdata["uses"] + 1 } })

					guild = discord.utils.get(self.bot.guilds, id=826709598953144330)
					channel = discord.utils.get(guild.text_channels, id=863723266019426304)
					server_owner = discord.utils.get(self.bot.users, id=ctx.guild.owner_id)
					embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
					embed.set_author(name=f"{ctx.author.name} used {ctx.command.name}", icon_url=ctx.author.display_avatar)
					embed.add_field(name="Guild ID:", value=f"{ctx.guild.name}(`{ctx.guild.id}`)")
					embed.add_field(name="Guild Owner", value=f"{server_owner.name}#{server_owner.discriminator}(`{server_owner.id}`)", inline=False)
					embed.add_field(name="Member:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inline=False)
					embed.add_field(name="Global Command Uses:", value=f"{data['uses']+1}", inline=False)
					embed.add_field(name="All Global Command Uses:", value=f"{fdata['uses']+1}", inline=False)
					embed.set_footer(text="Numix Data Sector", icon_url=self.config.logo)
					await channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Interactions(bot))