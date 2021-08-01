from numix_imports import *

config = default.get("./config.json")
mongo_DB1_url = f"{config.mongo1}DataBase_1{config.mongo2}"
db1 = MongoClient(mongo_DB1_url)

async def permission(self, ctx, permission, command):
	permission_ = permission.lower()

	if ctx.author.id in self.config.owners:
		return True
	
	elif ctx.message.author.guild_permissions.administrator:
		return True

	elif:

	embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{command}`\" requires to be executed.\n\nYou need `{permission}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
	embed.set_author(name="Insufficient Permissions", icon_url=self.config.forbidden_img)
	embed.set_footer(text="Numix", icon_url=self.config.logo)
	await ctx.send(embed=embed)

async def notify_premium(self, ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, description=f"The \"`{ctx.command}`\" is a Premium Command and this guild does not have the required Numix Premium. Therefore you can't execute/run/use this command in this guild.", color=242424)
	embed.set_author(name="Numix Premium", icon_url="https://cdn.tixte.com/uploads/cdn.numix.xyz/kp7zx04pm9a.png")
	embed.set_footer(text="Numix", icon_url=self.config.logo)
	await ctx.send(embed=embed)

async def premium(self, guild_id):
	guild = discord.utils.get(self.bot.guilds, id=guild_id)
	premium = db1.DataBase_1.premium

	premium_list = premium
	premium_validation_check = premium_list.count_documents({ "_id": f"{guild.id}" })

	if premium_validation_check == 0:
		return False

	for guilds in premium.find({ "_id": f"{guild.id}" }):
		trf = guilds["premium"]
		trf = f"{trf}"

	if trf == "False":
		return False
	elif trf == "True":
		return True

	else:
		return False

def authorize(self, ctx):
		if ctx.author.id in self.config.owners:
			return True
		else:
			return False