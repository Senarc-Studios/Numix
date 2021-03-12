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

		global_stats = await level.find_one({ '_id' : message.author.id })
		stats = await level.find_one({ '_id' : message.author.id, f"{message.guild.id}": { "id": message.guild.id } })
		if stats is None:
			newuser = {"_id": message.author.id, f"{message.guild.id}": { "id": message.guild.id, "level": 1, "xp": 0 }, "globallevel": 1, "globalxp": 0}
			await level.insert_one(newuser)

		elif global_stats is None:
			newuser = {"_id": message.author.id, f"{message.guild.id}": { "id": message.guild.id, "level": 1, "xp": 0 }, "globallevel": 1, "globalxp": 0}
			await level.insert_one(newuser)

		else:
			current_global_xp = global_stats['globalxp']
			current_guild_xp = stats['xp']
			new_global_xp = current_global_xp + 5
			new_guild_xp = current_guild_xp + 5
			await level.update_one({"_id": message.author.id}, {"$set": { f"{message.guild.id}": { "xp": new_guild_xp }, "globalxp": new_global_xp}}, upsert=True)

			guild_lvl = stats['level']
			if int( f" { stats['xp'] - guild_lvl * 2 * 100 } " ) >= round(guild_lvl * 2 * 100):
				new_lvl = guild_lvl + 1
				await level.update_one({ "_id": message.author.id }, { "$set": { f"{message.guild.id}": { "level": new_lvl } } }, upsert=True)
				await message.channel.send(f":tada: {message.author.mention} You leveled up to **Level {new_lvl}** :tada:")

			global_lvl = global_stats['level']
			if int( f" { global_stats['globalxp'] - global_lvl * 2 * 100 } " ) >= round(global_lvl * 2 * 100):
				new_lvl = global_lvl + 1
				await level.update_one({ "_id": message.author.id }, { "$set": { "globallevel": new_lvl } }, upsert=True)
				await message.channel.send(f":tada: {message.author.mention} You leveled up to **Level {new_lvl}** Globaly :tada:")

	@commands.command()
	async def rank(self, ctx, member: discord.Member=None):
		if member is None:
			member = ctx.author
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