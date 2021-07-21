import discord_webhook
from numix_imports import *
from numix_banking import *
from discord_webhook import DiscordWebhook
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, cooldown
import discord
import motor.motor_asyncio
import nest_asyncio # In case of asyncio errors

MONGO = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/Economy?retryWrites=true&w=majority"
cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGO)
WALLET_LIMIT = 50000
BANK_LIMIT = 1000000

class CustomCommand(commands.Command):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.perms = kwargs.get("perms", None)
        self.syntax = kwargs.get("syntax", None)

class economy(commands.Cog):
	def __init__(self, bot,):
		self.bot = bot
		self.config = default.get("./config.json")
		self.eco = cluster['Economy']['money']
		self.bank = cluster['Economy']['bank']
		self.bank_authorisation = cluster["Economy"]["credentials"]
		self.transaction_documents = cluster["Economy"]["transaction_logs"]

	async def create_account(self, id: int)-> None:
		wallet = {"_id": id, "bal": 100}
		bank_registration = { "_id": id, "bal": 0, "transactions": 0}
		await self.eco.insert_one(wallet)
		await self.bank.insert_one(bank_registration)

	async def register_account(self, id: int, password):

		credentials = { "_id": id, "password": password }
		await self.bank_authorisation.insert_one(credentials)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!shop [page]", description="List all the items in shop.", aliases=["sh", "shop-menu"])
	async def shop(self, ctx, page: int=1):
		try:
			page = int(page)
		except:
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"\"`{page}`\" is not a valid page, please enter a valid number, and there are only `{total_pages}` pages in total.", colour=242424)
			embed.set_author(name="Invalid Page", icon_url="https://cdn.iconscout.com/icon/free/png-512/cancel-1534469-1300531.png")
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			return await ctx.send(embed=embed)

		page = int(page)
		total_pages = 1
		if page == 1:
			embed = discord.Embed(timestamp=ctx.message.created_at, colour=242424)
			embed.set_author(name="Shopping Centre", icon_url=self.config.logo)
			embed.add_field(name="Item #0001", value="Description: A cookie that you can keep or give away. *(collectables)*\nPrice: $10", inline=False)
			embed.add_field(name="Item #0002", value="Description: Numix Premium redeem code for 1 day. *(investment)*\nPrice: $500000", inline=False)
			embed.add_field(name="Item #0003", value="Description: Worthless Token. *(collectables)*\nPrice: $20000", inline=False)
			embed.add_field(name="Item #0004", value="Description: Gucci Banana. *(collectables)*\nPrice: $10000", inline=False)
			embed.add_field(name="Item #0005", value="Description: 2x Global Levelling Booster. *(investment)*\nPrice: $5000", inline=False)
			embed.add_field(name="NOTE!", value="Keep in mind that this \"shop\" feature is still in beta and not released. So things might not work could be buggy.")
			embed.set_footer(text="Numix | Page 1/1", icon_url=self.config.logo)
			await ctx.send(embed=embed)

		else:
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"Page \"`{page}`\" is not a valid page in the shopping centre, there are only `{total_pages}` pages in total.", colour=242424)
			embed.set_author(name="Invalid Page", icon_url="https://cdn.iconscout.com/icon/free/png-512/cancel-1534469-1300531.png")
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!bal [member]", description="Check your account balance.", aliases=['balance','money','b', "wallet", "bank", "account", "open-account"])
	async def bal(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		id = member.id
		stats = await self.eco.find_one({'_id' : id})
		bank_account = await self.bank.find_one({ "_id": id })

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

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!work", description="Work command to get money.")
	@commands.cooldown(rate=1, per=15, type=BucketType.user)
	async def work(self, ctx):
		id = ctx.author.id
		wallet = await self.eco.find_one({ "_id": id })

		if wallet is None:
			return await ctx.send(f"{self.config.forbidden} Please open a account using `n!bal` command first.")

		job_list = ["Clerk", "Plumber", "Doctor", "Lumberjack", "Teacher", "Developer", "Slave", "Advertiser"]

		selected_job = random.choice(job_list)

		if selected_job == "Clerk":
			sallary = round(random.randint(323, 1512))
						
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You worked as a Clerk and the boss was generous enough to give you ${sallary} for your sallary. You can work again in 15 seconds.", color=242424)
			embed.set_author(name="Work", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			total_money = int(wallet["bal"] + sallary)

			if total_money > WALLET_LIMIT:
				return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

			await self.eco.update_one({ "_id": id }, { "$set": { "bal": total_money } })

			await ctx.send(embed=embed)

		elif selected_job == "Plumber":
			sallary = round(random.randint(100, 500))
						
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You worked as a Plumber and the boss was generous enough to give you ${sallary} for your sallary. You can work again in 15 seconds.", color=242424)
			embed.set_author(name="Work", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			total_money = int(wallet["bal"] + sallary)

			if total_money > WALLET_LIMIT:
				return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

			await self.eco.update_one({ "_id": id }, { "$set": { "bal": total_money } })

			await ctx.send(embed=embed)

		elif selected_job == "Doctor":
			sallary = round(random.randint(100, 1000))
						
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You worked as a Doctor and the patient was paid you ${sallary} for your sallary. You can work again in 15 seconds.", color=242424)
			embed.set_author(name="Work", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			total_money = int(wallet["bal"] + sallary)

			if total_money > WALLET_LIMIT:
				return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

			await self.eco.update_one({ "_id": id }, { "$set": { "bal": total_money } })

			await ctx.send(embed=embed)
		
		elif selected_job == "Lumberjack":
			sallary = round(random.randint(1000, 1500))
						
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You worked as a Lumberjack and the boss was generous enough to give you ${sallary} for your sallary. You can work again in 15 seconds.", color=242424)
			embed.set_author(name="Work", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			total_money = int(wallet["bal"] + sallary)

			if total_money > WALLET_LIMIT:
				return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

			await self.eco.update_one({ "_id": id }, { "$set": { "bal": total_money } })

			await ctx.send(embed=embed)

		elif selected_job == "Developer":
			sallary = round(random.randint(1000, 1500))
						
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You worked as a Developer and the boss was generous enough to give you ${sallary} for your sallary. You can work again in 15 seconds.", color=242424)
			embed.set_author(name="Work", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			total_money = int(wallet["bal"] + sallary)

			if total_money > WALLET_LIMIT:
				return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

			await self.eco.update_one({ "_id": id }, { "$set": { "bal": total_money } })

			await ctx.send(embed=embed)
			
		elif selected_job == "Slave":
			sallary = round(random.randint(100, 800))
						
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You worked as a Slave and the boss was generous enough to give you ${sallary} for your sallary. You can work again in 15 seconds.", color=242424)
			embed.set_author(name="Work", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			total_money = int(wallet["bal"] + sallary)

			if total_money > WALLET_LIMIT:
				return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

			await self.eco.update_one({ "_id": id }, { "$set": { "bal": total_money } })

			await ctx.send(embed=embed)

		elif selected_job == "Teacher":
			sallary = round(random.randint(180, 1000))
						
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You worked as a Teacher and the Principle was generous enough to give you ${sallary} for your sallary. You can work again in 15 seconds.", color=242424)
			embed.set_author(name="Work", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			total_money = int(wallet["bal"] + sallary)

			if total_money > WALLET_LIMIT:
				return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

			await self.eco.update_one({ "_id": id }, { "$set": { "bal": total_money } })

			await ctx.send(embed=embed)

		elif selected_job == "Advertiser":
			sallary = round(random.randint(10, 1000))
						
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You worked as a Advertiser and the company was generous enough to give you ${sallary} for your sallary. You can work again in 15 seconds.", color=242424)
			embed.set_author(name="Work", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)

			total_money = int(wallet["bal"] + sallary)

			if total_money > WALLET_LIMIT:
				return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

			await self.eco.update_one({ "_id": id }, { "$set": { "bal": total_money } })

			await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!daily", description="A command to get your daily money.")
	@commands.cooldown(rate=1, per=86400, type=BucketType.user)
	async def daily(self, ctx):
		id = ctx.author.id
		wallet = await self.eco.find_one({ "_id": id })

		drop_chance = ["100", "200", "300", "100", "100", "100", "200", "200", "200", "300", "300", "300", "300", "500", "500", "500", "1000", "1000", "1000", "10000", "100", "200", "300", "100", "100", "100", "200", "200", "200", "300", "300", "300", "300", "500", "500", "500", "1000", "1000", "1000", "10000", "100", "200", "300", "100", "100", "100", "200", "200", "200", "300", "300", "300", "300", "500", "500", "500", "1000", "1000", "1000", "10000"]
		random_drop = random.choice(drop_chance)

		if wallet is None:
			return await ctx.send(f"{self.config.forbidden} Please open a account using `n!bal` command first.")

		earned_money = wallet["bal"] + int(random_drop)
		if 50000 < earned_money:
			return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

		await self.eco.update_one({ "_id": id }, { "$set": { "bal": earned_money } })
		e = discord.Embed(timestamp=ctx.message.created_at, description=f"You got **${random_drop}**\n\nYou can get your daily cash in the next 24 hours.", color=242424)
		e.set_author(name="Daily Cash", icon_url=ctx.author.avatar_url)
		e.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=e)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!monthly", description="A command to get your monthly money.")
	@commands.cooldown(rate=1, per=2592000, type=BucketType.user)
	async def monthly(self, ctx):
		id = ctx.author.id
		wallet = await self.eco.find_one({ "_id": id })

		if wallet is None:
			return await ctx.send(f"{self.config.forbidden} Please open a account using `n!bal` command first.")

		drop_chance = ["20000", "20000", "20000", "20000", "20000", "20000", "100", "600", "699", "1000", "100", "600", "100", "600", "699", "1000", "100", "600", "100", "600", "699", "1000", "100", "600", "100", "600", "699", "1000", "100", "600", "100", "600", "699", "1000", "100", "600", "100", "600", "699", "1000", "100", "600"]
		random_drop = random.choice(drop_chance)

		earned_money = wallet["bal"] + int(random_drop)
		if 50000 < earned_money:
			return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can deposit your money in your bank.")

		await self.eco.update_one({ "_id": id }, { "$set": { "bal": earned_money } })
		e = discord.Embed(timestamp=ctx.message.created_at, description=f"You got **${random_drop}**\n\nYou can get your daily cash in the next 30 days.", color=242424)
		e.set_author(name="Monthly Cash", icon_url=ctx.author.avatar_url)
		e.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=e)
		

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!withdraw <money>", description="Withdraw money from your bank account.", aliases=["cash-out", "with"])
	async def withdraw(self, ctx, money=None):
		username = ctx.author.id
		id = username
		bank_account = await self.bank.find_one({ "_id": id })
		wallet = await self.eco.find_one({ "_id": username })

		if wallet is None:
			return await ctx.send(f"{self.config.forbidden} Please open a account using `n!bal` command first.")

		if money == "all":
			money = wallet["bal"]

		else:
			money = int(money)

		if money is None:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} Specify the ammount of money to be withdrawn.")

		if money <= 10:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} You can't withdraw money less than $10.")

		if bank_account["bal"] < money:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} You have reached the max level of funds on your Bank Account.")

		earned_money = money+bank_account["bal"]
		if 50000 < earned_money:
			return await ctx.send(f"{self.config.forbidden} Your wallet will be full, you can't withdraw that much money.")

		await self.bank.update_one({ "_id": username }, { "$set": { "bal": int(bank_account["bal"])-money } })
		await self.eco.update_one({ "_id": username }, { "$set": { "bal": int(wallet["bal"])+money } })

		await ctx.send(f"{self.config.success} {ctx.author.mention} Your money has been withdrawn.")

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!deposit <amount>", description="Deposit money to your bank account.", aliases=["dep", "depo"])
	async def deposit(self, ctx, money=None):
		username = ctx.author.id
		id = username
		bank_authorisation = await self.bank_authorisation.find_one({ "_id": username })
		bank_account = await self.bank.find_one({ "_id": username })
		wallet = await self.eco.find_one({ "_id": username })

		if money is None:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} Specify the ammount of money to be deposited.")

		if money == "all":
			money = wallet["bal"]

		else:
			money = int(money)

		if money > wallet["bal"]:
			return await ctx.send(f"{self.config.forbidden} You don't have enough money in your wallet.")

		if money <= 10:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} You can't send money less than $10.")

		if bank_account["bal"] >= 999990:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} You have reached the max level of funds on your Bank Account.")

		await self.bank.update_one({ "_id": username }, { "$set": { "bal": int(bank_account["bal"])+money } })
		await self.eco.update_one({ "_id": username }, { "$set": { "bal": int(wallet["bal"])-money } })

		await ctx.send(f"{self.config.success} {ctx.author.mention} Your money has been deposited.")

	@commands.command(cls=CustomCommand, description="Change the password of your bank account.", aliases=["cp", "change-pswrd", "change-pass", "change-password"])
	async def changepassword(self, ctx, current_password=None, new_password=None):
		bank_auth = await self.bank_authorisation.find_one({ "_id": ctx.author.id })
		if current_password is None:
			return await ctx.send(f"{self.config.forbidden} Specify your current password and your new password.")

		elif new_password is None:
			return await ctx.send(f"{self.config.forbidden} Specify your new password.")

		elif current_password != bank_auth["password"]:
			return await ctx.send(f"{self.config.forbidden} The credentials you've entered isn't valid.")

		await self.bank_authorisation.update_one({ "_id": ctx.author.id }, { "$set": { "password": f"{new_password}" } })
		await ctx.message.delete()
		await ctx.send(f"{self.config.success} {ctx.author.mention} Your password has been changed.")

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!pay <username> <password> <money> <receiver>", description="Send/Pay money to someone else", aliases=["send-money", "transfer", "sm"])
	async def pay(self, ctx, username: int=None, password=None, money: int=None, receiver: int=None):
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
		bank_account = await self.bank_authorisation.find_one({ "_id": id })
		recipient = await self.bank_authorisation.find_one({ "_id": receiver })
		bank_loggedin = await self.bank.find_one({ "_id": id })
	
		if username is None:
			return await ctx.send(f"To transfer the money to another account, please use the right formate.\n\n**Formate:**\n`n!sm <username> <password> <money> <uora>`\n\nThe Username is going to be the User ID of the account/user you're sending it from, and the Password is the password of that account. UORA means Username Of Receiving Account, which is the username of the receiving account.")

		elif password is None:
			return await ctx.send(f"{self.config.forbidden} The credentials you've entered isn't valid.")

		elif username == receiver:
			return await ctx.send(f"{self.config.forbidden} You can't send money to yourself.") 

		elif password != bank_account["password"]:
			return await ctx.send(f"{self.config.forbidden} The credentials you've entered isn't valid.")

		elif money is None:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} Specify the ammount of money to be sent.")

		elif money <= 10:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} You can't send money less than $10.")

		elif receiver is None:
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
		recipient_account = await self.bank.find_one({ "_id": receiver })

		generated = generate_transaction_id()
		convert_to_string = f"{generated}"
		transaction_id = f"{convert_to_string}"

		generated_1 = generate_transaction_id()
		convert_to_string_1 = f"{generated_1}"
		transaction_id_1 = f"{convert_to_string_1}"

		if bank_ballance < money:
			await ctx.message.delete()
			return await ctx.send(f"{self.config.forbidden} This account doesn't have enough Funds to send money.")

		total_money = recipient_account["bal"] + money

		if total_money > BANK_LIMIT:
			if receiver not in self.config.break_bank_limit:
				await ctx.message.delete()
				return await ctx.send(f"{self.config.forbidden} The recipient has reached the max level of funds.")

		await ctx.message.delete()

		await self.bank.update_one({ "_id": username }, { "$set": { "bal": int(bank_ballance)-money, "transactions": int(bank_transactions)+1 } })
		await self.bank.update_one({ "_id": receiver }, { "$set": { "bal": int(recipient_account["bal"])+money, "transactions": int(recipient_account["transactions"])+1 } })

		await self.transaction_documents.insert_one({ "_id": f"{transaction_id}", "account_owner": username, "recipient": receiver, "money": f"-${money}", "time": f"{ctx.message.created_at.__format__('%H:%M:%S')}", "date": f"{Today}" })
		await self.transaction_documents.insert_one({ "_id": f"{transaction_id_1}", "account_owner": receiver, "recipient": username, "money": f"+${money}", "time": f"{ctx.message.created_at.__format__('%H:%M:%S')}", "date": f"{Today}" })

		account_owner = discord.utils.get(self.bot.users, id=id)
		recipient_user = discord.utils.get(self.bot.users, id=receiver)

		
		msg = f"{account_owner.name}#{account_owner.discriminator}(`{account_owner.id}`) has bank transfered ${money} to {recipient_user.name}#{recipient_user.discriminator}(`{recipient_user.id}`) at {Today} {ctx.message.created_at}. Owner account trasaction ID is `{transaction_id}`, Recipient account transaction ID is `{transaction_id_1}`."
		webhook = DiscordWebhook(url="https://ptb.discord.com/api/webhooks/827106209105838091/4h1OhWgyUZyAbaxf29LRpoE4bdobl8qzyzdG1-SfINVtRSC854M5OIxncdTi-87rxPYn", content=msg)
		response = webhook.execute()
		print(response)

		e = discord.Embed(timestamp=ctx.message.created_at, description="If you did not send the money, you can contact the **Numix Fraud Deparment**.", color=242424)
		e.set_author(name="Money Sent", icon_url=account_owner.avatar_url)
		e.add_field(name="Ammount of Money Sent:", value=f"${money}", inline=False)
		e.add_field(name="Recipient:", value=f"{recipient_user.name}#{recipient_user.discriminator}(`{recipient_user.id}`)", inline=False)
		e.add_field(name="Transaction ID:", value=f"`{transaction_id}`", inline=False)
		e.set_footer(text="Numix", icon_url=self.config.logo)
		await account_owner.send(embed=e)

		em = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		em.set_author(name="Money Received", icon_url=recipient_user.avatar_url)
		em.add_field(name="Ammount of Money Received:", value=f"${money}", inline=False)
		em.add_field(name="Sent by:", value=f"{account_owner.name}#{account_owner.discriminator}(`{account_owner.id}`)", inline=False)
		em.add_field(name="Transaction ID:", value=f"`{transaction_id_1}`", inline=False)
		em.set_footer(text="Numix", icon_url=self.config.logo)
		await recipient_user.send(embed=em)

		await ctx.send(f"{self.config.success} {ctx.author.mention} Transaction is Complete")
		
def setup(bot):
	bot.add_cog(economy(bot))