from numix_imports import *
from numix_banking import *
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, cooldown
import discord
import motor.motor_asyncio
import nest_asyncio # In case of asyncio errors

MONGO = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/Economy?retryWrites=true&w=majority"


cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGO)
eco = cluster['Economy']['money']
bank = cluster['Economy']['bank']
bank_authorisation = cluster["Economy"]["credentials"]
transaction_documents = cluster["Economy"]["transaction_logs"]

class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")

	async def create_account(self, id: int)-> None:
		wallet = {"_id": id, "bal": 100}
		bank_registration = { "_id": id, "bal": 0, "transactions": 0}
		await eco.insert_one(wallet)
		await bank.insert_one(bank_registration)

	async def register_account(self, id: int, password):

		credentials = { "_id": id, "password": password }
		await bank_authorisation.insert_one(credentials)

	@commands.command(aliases=['balance','money','b', "wallet", "bank", "account"])
	async def bal(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		id = member.id
		stats = await eco.find_one({'_id' : id})
		bank_account = await bank.find_one({ "_id": id })

		if stats is None:
			generate = generate_bank_password()
			convert_to_string = f"{generate}"
			password = f"{convert_to_string}"

			await self.create_account(id)
			await self.register_account(id, password)

			em = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			em.set_author(name=f"Bank Account", icon_url=self.config.logo)
			em.add_field(name="Username:", value=f"{member.id}", inline=False)
			em.add_field(name="Password:", value=f"{password}", inline=False)
			em.set_footer(text="Numix", icon_url=self.config.logo)

			await member.send(embed=em)

			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name=f'{member.name}\'s Account', icon_url=member.avatar_url)
			e.add_field(name="Wallet:", value=f"$100", inline=False)
			e.add_field(name="Bank Ballance:", value=f"$0", inline=False)
			e.add_field(name="Bank Transactions:", value=f"`0`", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)

			await ctx.send(embed=e)

		else:
			money = stats['bal']
			bank_ballance = bank_account["bal"]
			bank_transactions = bank_account["transactions"]

			e = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			e.set_author(name=f'{member.name}\'s Account', icon_url=member.avatar_url)
			e.add_field(name="Wallet:", value=f"${money}", inline=False)
			e.add_field(name="Bank Ballance:", value=f"${bank_ballance}", inline=False)
			e.add_field(name="Bank Transactions:", value=f"`{bank_transactions}`", inline=False)
			e.set_footer(text="Numix", icon_url=self.config.logo)

			await ctx.send(embed=e)

	@commands.command(aliases=["send-money", "transfer", "pay"])
	async def sm(self, ctx, username: int=None, password=None, money: int=None, receiver: int=None):
		date_1 = f"{ctx.message.created_at.__format__('%d-%B-%Y')}"
		date_2 = date_1.replace("January", "01")
		date_3 = date_2.replace("February", "02")
		date_4 = date_3.replace("March", "03")
		date_5 = date_4.replace("April", "04")
		date_6 = date_5.replace("May", "05")
		date_7 = date_6.replace("June", "06")
		date_8 = date_7.replace("July", "07")
		date_9 = date_8.replace("August", "08")
		date_10 = date_9.replace("September", "09")
		date_11 = date_10.replace("October", "10")
		date_12 = date_11.replace("November", "11")
		date_13 = date_12.replace("December", "12")
		Today = date_13

		id = username
		bank_account = await bank_authorisation.find_one({ "_id": id })
		recipient = await bank_authorisation.find_one({ "_id": receiver })
		bank_loggedin = await bank.find_one({ "_id": id })
	
		if username is None:
			return await ctx.send(f"To transfer the money to another account, please use the right formate.\n\n**Formate:**\n`n!sm <username> <password> <money> <uora>`\n\nThe Username is going to be the User ID of the account/user you're sending it from, and the Password is the password of that account. UORA means Username Of Receiving Account, which is the username of the receiving account.")

		if password is None:
			return await ctx.send(f"{self.config.forbidden} The credentials you've entered isn't valid.")

		if password != bank_account["password"]:
			return await ctx.send(f"{self.config.forbidden} The credentials you've entered isn't valid.")

		if money is None:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} Specify the ammount of money to be sent.")

		if money <= 10:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} You can't send money less than $10.")

		if receiver is None:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} Specify a valid username of the account that is receiving the money.")

		try:
			if recipient["password"] is None:
				await ctx.message.delete()
				return await ctx.send(f"{self.config.forbidden} Specify a valid username of the account that is receiving the money.")
		except Exception as e:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} Specify a valid username of the account that is receiving the money.")

		bank_ballance = bank_loggedin["bal"]
		bank_transactions = bank_loggedin["transactions"]
		recipient_account = await bank.find_one({ "_id": receiver })

		generated = generate_transaction_id()
		convert_to_string = f"{generated}"
		transaction_id = f"{convert_to_string}"

		generated_1 = generate_transaction_id()
		convert_to_string_1 = f"{generated_1}"
		transaction_id_1 = f"{convert_to_string_1}"

		if bank_ballance < money:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} This account doesn't have enough Funds to send money.")

		if recipient_account["bal"] >= 999990:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} The recipient has reached the max level of funds.")

		await ctx.message.delete()

		await bank.update_one({ "_id": username }, { "$set": { "bal": int(bank_ballance)-money, "transactions": int(bank_transactions)+1 } })
		await bank.update_one({ "_id": receiver }, { "$set": { "bal": int(recipient_account["bal"])+money, "transactions": int(recipient_account["transactions"])+1 } })

		await transaction_documents.insert_one({ "_id": f"{transaction_id}", "account_owner": username, "recipient": receiver, "money": f"-${money}", "time": f"{ctx.message.created_at.__format__('%H:%M:%S')}", "date": f"{Today}" })
		await transaction_documents.insert_one({ "_id": f"{transaction_id_1}", "account_owner": receiver, "recipient": username, "money": f"+${money}", "time": f"{ctx.message.created_at.__format__('%H:%M:%S')}", "date": f"{Today}" })
		
		account_owner = discord.utils.get(self.bot.users, id=id)
		recipient_user = discord.utils.get(self.bot.users, id=receiver)

		e = discord.Embed(timestamp=ctx.message.created_at, description="If you did not send the money, you can contact the **Numix Fraud Deparment**.", color=242424)
		e.set_author(name="Money Sent", icon_url=account_owner.avatar_url)
		e.add_field(name="Ammount of Money Sent:", value=f"{money}", inline=False)
		e.add_field(name="Recipient:", value=f"{recipient_user.name}#{recipient_user.discriminator}(`{recipient_user.id}`)", inline=False)
		e.add_field(name="Transaction ID:", value=f"`{transaction_id}`", inline=False)
		e.set_footer(text="Numix", icon_url=self.config.logo)
		await account_owner.send(embed=e)

		em = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		em.set_author(name="Money Received", icon_url=recipient_user.avatar_url)
		em.add_field(name="Ammount of Money Received:", value=f"{money}", inline=False)
		em.add_field(name="Sent by:", value=f"{account_owner.name}#{account_owner.discriminator}(`{account_owner.id}`)", inline=False)
		em.add_field(name="Transaction ID:", value=f"`{transaction_id_1}`", inline=False)
		em.set_footer(text="Numix", icon_url=self.config.logo)
		await recipient_user.send(embed=em)

		await ctx.send(f"{self.config.success} {ctx.author.mention} Transaction is Complete")
		
def setup(bot):
	bot.add_cog(Economy(bot))