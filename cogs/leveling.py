from numix_imports import *
import motor.motor_asyncio
import discord

mongo_url = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
level = cluster["DataBase_1"]['Leveling']

class Leveling(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		print('"Leveling" cog loaded')


	@commands.Cog.listener()
	async def on_message(self, message):

		if message.author.bot:
			return

		elif message.guild is None:
			return 

		# Checks for dm and bot 

		stats = await level.find_one({'_id' : message.author.id})
		try:
			if stats is None:
				newuser = {"_id": message.author.id, "GuildID": message.guild.id,"Level" : 1,"XP": 0}
				await level.insert_one(newuser)

			else:
				current_xp = stats['XP']
				new_xp = current_xp + 5
				await level.update_one({"_id": message.author.id}, {"$set": {"XP": new_xp}})

				lvl_start = stats['Level']
				if stats['XP'] >= round(lvl_start * 2 * 100):
					new_lvl  = lvl_start + 1
					await level.update_one({"_id": message.author.id}, {"$set": {"Level": new_lvl}})
					await message.channel.send(f":tada: {message.author.mention} You leveled up to **Level {new_lvl}** :tada:")

		except Exception:
			pass

	@commands.command()
	async def rank(self, ctx, member: discord.Member=None):
		if member is None:
			member = ctx.author
		else:
			pass
		try:
			stats = await level.find_one({'_id' : member.id, "GuildID": ctx.guild.id})
			if stats is None:
				newuser = {"_id": member.id, "GuildID": ctx.guild.id, "Level" : 1, "XP": 0}
				await level.insert_one(newuser)

			else:
				xp = stats['XP']
				lvl = stats['Level']
				embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
				embed.set_author(name=f"{member.name}'s Rank", icon_url=member.avatar_url)
				embed.set_thumbnail(url=ctx.guild.icon_url)
				embed.add_field(name='Level:',value=f'{lvl}', inline=False)
				embed.add_field(name='Total XP:',value=f'{xp}', inline=False)
				embed.add_field(name="XP to next level:", value=int((lvl * 2 * 100)-xp), inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(f"{member.mention}'s rank commands has been loaded.", delete_after=0)
				await ctx.send(embed=embed)


		except Exception:
			pass

def setup(bot):
	bot.add_cog(Leveling(bot))