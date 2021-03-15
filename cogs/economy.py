from numix_imports import *
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, cooldown
import discord
import motor.motor_asyncio
import nest_asyncio # In case of asyncio errors

MONGO = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/Economy?retryWrites=true&w=majority"


cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGO)
eco = cluster['Economy']['money']


class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")

	async def create_account(self,id : int)-> None:
		"""
		Function to make opening account easy
		"""
		newuser = {"_id": id, "bal": 100}
		await eco.insert_one(newuser)


	@commands.command(aliases=['balance','money','b'])
	async def bal(self,ctx,member : discord.Member = None):
		"""
		Command to see your balance
		"""
		if member is None:
			member = ctx.author

		id = member.id
		stats = await eco.find_one({'_id' : id})

		if stats is None:
			self.create_account(id)
			await ctx.send('**No data found**')
		else:
			money = stats['bal']
			e = discord.Embed()
			e.add_field(name=f'{member.mention} Wallet', value=f"{member.name} has {money}")

			await ctx.send(embed=e)

		
def setup(bot):
	bot.add_cog(Economy(bot))