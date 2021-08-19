from numix_imports import *
from collections import OrderedDict, deque, Counter
import motor.motor_asyncio
import os

config = default.get('./config.json')

def badges(self, id: int):
	collection = MONGO.DataBase_1.assets
	premium_collection = MONGO.DataBase_1.premium
	premium_users = []
	MONGO = MongoClient(f"{config.db1}")
	
	for data in collection.find({ "_id": "badges" }):
		for server in self.bot.guilds:
			if premium_collection.count_documents({ "_id": f"{server.id}", "premium": "True" }) == 1:
				owner_id = server.owner_id
				premium_users.append(owner_id)

		all_badges = ""
		if id in config.owners:
			all_badges = all_badges + " " + config.developer
		
		if id in data["partnered_users"]:
			all_badges = all_badges + " " + config.partnered

		if id in data["verified_users"]:
			all_badges = all_badges + " " + config.verified

		if id in data["beta_testers"]:
			all_badges = all_badges + " " + config.beta_tester

		if id in premium_users:
			all_badges = all_badges + " " + config.premium

	return f"{all_badges} <:members:877398159368814623>"

def format_dt(dt, style=None):
	if style is None:
		return f'<t:{int(dt.timestamp())}>'
	return f'<t:{int(dt.timestamp())}:{style}>'

def format_relative(dt):
	return format_dt(dt, 'R')

def permission(permission):

	async def predicate(ctx):
		if ctx.author.id in config.owners:
			return True

		elif permission == "administrator":
			if ctx.author.guild_permissions.administrator:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "manage_messages":
			if ctx.author.guild_permissions.manage_messages:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "kick":
			if ctx.author.guild_permissions.kick:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "ban":
			if ctx.author.guild_permissions.ban:
				return True
				
			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "manage_guild":
			if ctx.author.guild_permissions.manage_guild:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)
		

	return commands.check(predicate)

MONGO = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"
cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGO)
leveling = cluster["DataBase_1"]['Leveling']

class CustomCommand(commands.Command):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.perms = kwargs.get("perms", None)
		self.syntax = kwargs.get("syntax", None)

def countlines(rootdir, total_lines=0, header=False, begin_start=None, code_only=False):
	def _get_new_lines(source):
		total = len(source)
		i = 0
		while i < len(source):
			line = source[i]
			trimline = line.lstrip(" ")

			if trimline.startswith('#') or trimline == '':
				total -= 1
			elif '"""' in trimline:	# docstring begin
				if trimline.count('"""') == 2:	# docstring end on same line
					total -= 1
					i += 1
					continue
				doc_start = i
				i += 1
				while '"""' not in source[i]:	# docstring end
					i += 1
				doc_end = i
				total -= (doc_end - doc_start + 1)
			i += 1
		return total

	if header:
		print('{:>10} |{:>10} | {:<20}'.format('ADDED', 'TOTAL', 'FILE'))
		print('{:->11}|{:->11}|{:->20}'.format('', '', ''))

	for name in os.listdir(rootdir):
		file = os.path.join(rootdir, name)
		if os.path.isfile(file) and file.endswith('.py'):
			with open(file, 'r') as f:
				source = f.readlines()

			if code_only:
				new_lines = _get_new_lines(source)
			else:
				new_lines = len(source)
			total_lines += new_lines

			if begin_start is not None:
				reldir_of_file = '.' + file.replace(begin_start, '')
			else:
				reldir_of_file = '.' + file.replace(rootdir, '')

			print('{:>10} |{:>10} | {:<20}'.format(
					new_lines, total_lines, reldir_of_file))

	for file in os.listdir(rootdir):
		file = os.path.join(rootdir, file)
		if os.path.isdir(file):
			total_lines = countlines(file, total_lines, header=False, begin_start=rootdir, code_only=code_only)
	return total_lines

class general(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
		self.process = psutil.Process(os.getpid())
		self.mongo_moderation_url = f"{self.config.mongo1}Moderation{self.config.mongo2}"
		self.moderation_db = MongoClient(self.mongo_moderation_url)
		self.mongo_DB1_url = f"{self.config.mongo1}DataBase_1{self.config.mongo2}"
		self.db1 = MongoClient(self.mongo_DB1_url)
		print('"Info" cog loaded')

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!profile <edit/member> [bio]", description="Show other's profile or edit your profile.", aliases=["prfil", "profil"])
	async def profile(self, ctx, option=None, *, bio=None):
		if option == None:
			option = ctx.author

			collection = self.db1.DataBase_1.profiles
			if collection.count_documents({ "_id": option.id }) == 0:

				embed = discord.Embed(timestamp=ctx.message.created_at, colour=242424)
				embed.set_author(name=f"{option.name}'s Profile", icon_url=option.avatar_url)
				embed.add_field(name="Numix Badges", value=badges(self, option.id))
				embed.add_field(name="Bio", value=f"{self.config.arrow} No bio set.", inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				return await ctx.send(embed=embed)

			for data in collection.find({ "_id": int(option.id) }):
				bio = data["bio"]
				embed = discord.Embed(timestamp=ctx.message.created_at, colour=242424)
				embed.set_author(name=f"{option.name}'s Profile", icon_url=option.avatar_url)
				embed.add_field(name="Numix Badges", value=badges(self, option.id))
				embed.add_field(name="Bio", value=f"{self.config.arrow} {bio}", inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)

		elif option.startswith("<@!"):
			option = option.replace("<@!", "")
			option = option.replace(">", "")
			option = discord.utils.get(self.bot.users, id=int(option))

			collection = self.db1.DataBase_1.profiles
			if collection.count_documents({ "_id": option.id }) == 0:

				embed = discord.Embed(timestamp=ctx.message.created_at, colour=242424)
				embed.set_author(name=f"{option.name}'s Profile", icon_url=option.avatar_url)
				embed.add_field(name="Numix Badges", value=badges(self, option.id))
				embed.add_field(name="Bio", value=f"{self.config.arrow} No bio set.", inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				return await ctx.send(embed=embed)

			for data in collection.find({ "_id": int(option.id) }):
				bio = data["bio"]
				embed = discord.Embed(timestamp=ctx.message.created_at, colour=242424)
				embed.set_author(name=f"{option.name}'s Profile", icon_url=option.avatar_url)
				embed.add_field(name="Numix Badges", value=badges(self, option.id))
				embed.add_field(name="Bio", value=f"{self.config.arrow} {bio}", inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)

		elif option == "edit":
			if bio == None:
				return await ctx.send(f"{self.config.forbidden} Please specify your new bio.")

			if len(bio) >= 300:
				return await ctx.send(f"{self.config.forbidden} Your bio can't be longer than 300 characters.")

			collection = self.db1.DataBase_1.profiles
			if collection.count_documents({ "_id": int(ctx.author.id) }) == 0:
				collection.insert_one({ "_id": int(ctx.author.id), "bio": bio })

				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"Your bio has been updated from `No bio set.` to `{bio}`", colour=242424)
				embed.set_author(name="Bio Updated", icon_url=ctx.author.avatar_url)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)
			
			else:
				collection.update_one({ "_id": int(ctx.author.id) }, { "$set": { "_id": int(ctx.author.id), "bio": bio } })
				for data in collection.find({ "_id": int(ctx.author.id) }):
					old_bio = data["bio"]

					embed = discord.Embed(timestamp=ctx.message.created_at, description=f"Your bio has been updated from `{old_bio}` to `{bio}`", colour=242424)
					embed.set_author(name="Bio Updated", icon_url=ctx.author.avatar_url)
					embed.set_footer(text="Numix", icon_url=self.config.logo)
					await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!skin", description="Gets a Minecraft Skin of a player.", aliases=[ "mc-skin", "mc-user", "player", "mc-player", "mc-name", "uuid" ])
	async def skin(self, ctx, username=None):
		if username == None:
			return await ctx.send(f"{self.config.forbidden} Specify a Username to get the skin.")
		uuid = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'.format(username)).json()['id']

		url = json.loads(base64.b64decode(requests.get('https://sessionserver.mojang.com/session/minecraft/profile/{}'.format(uuid)).json()['properties'][0]['value']).decode('utf-8'))['textures']['SKIN']['url']
	
		names = requests.get('https://api.mojang.com/user/profiles/{}/names'.format(uuid)).json()
		history = "**Name History:**\n"
		for name in reversed(names):
			history += name['name']+"\n"

		embed = discord.Embed(timestamp=ctx.message.created_at, colour=242424)
		embed.set_author(name=f"Results for {username}", icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"UUID:", value=f"`{uuid}`")
		embed.set_image(url=f"{url}")
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!emoji <emoji_name>", description="Get's the ID and tag of the emoji.", aliases=["emoji-id", "eid", "emoid", "emojiid", "emoji_id"])
	async def emoji(self, ctx, *, emoji=None):
		if emoji == None:
			return await ctx.send(f"{self.config.forbidden} Please provide a emoji name as a parameter.")

		emojis = emoji.split(" ")
		emoji_tags = []

		for i in emojis:
			try:
				emoji = discord.utils.get(self.bot.emojis, name=i)
				emoji_tags.append(f"**Static:** <:{emoji.name}:{emoji.id}>\n**Animated:** <a:{emoji.name}:{emoji.id}>")
				continue
			except:
				emoji_tags.append(f"{self.config.forbidden} `unable to find emoji \"{i}\"`")
				continue

		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_author(name="Emoji Query", icon_url=ctx.author.avatar_url)
		for i in emoji_tags:
			for a in emojis:
				embed.add_field(name=f"{a}", value=i, inline=False)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!discriminator [discriminator]", description="Get's people who have a discriminator that you asked.", aliases=["discrim", "discrm", "disc"])
	async def discriminator(self, ctx, discriminator=None):
		try:
			if discriminator == None:
				discriminator = str(ctx.author.discriminator)
			
			else:
				discriminator = discriminator.replace("#", "")
				discriminator = discriminator
			
			disc_list = list(discriminator)
			count = 0
			
			for i in disc_list:
				count = count + 1

			for i in disc_list:
				
				if i == "0" or i == "1" or i == "2" or i == "3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9":
					continue

				else:
					return await ctx.send(f"{self.config.forbidden} Enter a valid discriminator.")

			if count > 4 or count < 4:
				return await ctx.send(f"{self.config.forbidden} Enter a valid discriminator.")
	
		except:
			return await ctx.send(f"{self.config.forbidden} Enter a valid discriminator.")

		count = 1
		discs = ""
		
		for i in self.bot.users:
			if i.discriminator == discriminator:
				discs = discs + f"**{count}.** `{i.name}#{i.discriminator}`\n\n"
				count = count + 1
			if count == 6:
				break

		embed = discord.Embed(timestamp=ctx.message.created_at, description=f"{discs}", colour=242424)
		embed.set_author(name=f"Users with Discriminator #{discriminator}", icon_url=self.config.logo)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!rank [member]", description="Gets information of the user's rank.", aliases=["level", "xp"])
	async def rank(self, ctx, user: discord.Member=None):
		if user is None:
			user = ctx.message.author
		
		if await leveling.count_documents({ "_id": user.id, f"{ctx.guild.id}": "ENABLED" }) == 0:
			if user.id == ctx.author.id:
				return await ctx.send(f"{self.config.forbidden} Please send some message before checking your rank.")
			return await ctx.send(f"{self.config.forbiden} {user.name} hasn't sent any messages yet.")

		user_data = await leveling.find_one({ "_id": user.id })
		GLOBAL_FORMULA = int((50 * (user_data[f"GLOBAL_LEVEL"] ** 2)) + (50 * user_data[f"GLOBAL_LEVEL"]))
		GLOBAL_BAR = int(( -(GLOBAL_FORMULA)/(200*((1/2) * user_data[f"GLOBAL_LEVEL"])))*20)
		GLOBAL_RANKING = leveling.find().sort("TOTAL_XP", -1)

		GUILD_FORMULA = int((50 * (user_data[f"{ctx.guild.id}_LEVEL"] ** 2)) + (50 * user_data[f"{ctx.guild.id}_LEVEL"]))
		GUILD_BAR = int(( -(GUILD_FORMULA)/(200*((1/2) * user_data[f"{ctx.guild.id}_LEVEL"])))*20)
		GUILD_RANKING = leveling.find().sort(f"{ctx.guild.id}_TOTAL_XP", -1)

		embed = discord.Embed(timestamp=ctx.message.created_at)
		embed.set_author(name=f"{user.name}'s Rank", icon_url=user.avatar_url)
		embed.add_field(name="Level:", value=f"{user_data[f'{ctx.guild.id}_LEVEL']}")
		embed.add_field(name="XP:", value=f"`{user_data[f'{ctx.guild.id}_XP']}xp`")
		embed.add_field(name="Progress Bar:", value=GUILD_BAR * "<:blue_box:854277153809760277>" + (20-GUILD_BAR) * "<:Box:854277154032582658>", inline=False)
		embed.add_field(name="Global Level:", value=f"{user_data[f'GLOBAL_LEVEL']}")
		embed.add_field(name="Global XP:", value=f"`{user_data[f'GLOBAL_XP']}xp`")
		embed.add_field(name="Global Progress Bar:", value=GLOBAL_BAR * "<:blue_box:854277153809760277>" + (20-GLOBAL_BAR) * "<:Box:854277154032582658>", inline=False)
		embed.set_thumbnail(url=user.avatar_url)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!leaderboard [type]", description="Shows leaderboard of specified type.", aliases=["lb", "board", "rankings"])
	async def leaderboard(self, ctx, type=None):
		if type == None:
			rankings = leveling.find().sort(f"{ctx.guild.id}_TOTAL_XP", -1)
			i = 1
			embed = discord.Embed(timestamp=ctx.message.created_at, title="Leaderboard:")
			for x in rankings:
				try:
					temp = ctx.guild.get_member(x["_id"])
					tempxp = x[f"{ctx.guild.id}_TOTAL_XP"]
					embed.add_field(name=f"{i}: {temp.name}", value=f"XP: `{tempxp}`", inline=False)
					i += 1
				except:
					pass
				if 1 == 11:
					break
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)

		elif type == "global":
			rankings = leveling.find().sort("TOTAL_XP", -1)
			i = 1
			embed = discord.Embed(timestamp=ctx.message.created_at, title="Leaderboard:")
			for x in rankings:
				try:
					temp = discord.utils.get(self.bot.users, x["_id"])
					tempxp = x[f"TOTAL_XP"]
					embed.add_field(name=f"{i}: {temp.name}", value=f"XP: `{tempxp}`", inline=False)
					i += 1
				except:
					pass
				if 1 == 11:
					break
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!premium [server]", description="Checks if a server has Numix Premium enabled.")
	async def premium(self, ctx, id=None):
		if id is None:
			id = ctx.guild.id

		deactivated_premium = "https://cdn.tixte.com/uploads/cdn.numix.xyz/kp80894na9a.png"
		activated_premium = "https://cdn.tixte.com/uploads/cdn.numix.xyz/kp7zx04pm9a.png"

		premium = self.db1.DataBase_1.premium

		premium_list = premium
		premium_validation_check = premium_list.count_documents({ "_id": f"{id}" })

		if premium_validation_check == 0:
			e = discord.Embed(timestamp=ctx.message.created_at, description=f"Premium is not activated and premium commands can't be executed in the server.", color=0xB8B8B8)
			e.set_author(name="Numix Premium", icon_url=deactivated_premium)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			return await ctx.send(embed=e)

		for guilds in premium.find({ "_id": f"{id}" }):
			trf = guilds["premium"]
			trf = f"{trf}"

		if trf == "False":
			e = discord.Embed(timestamp=ctx.message.created_at, description=f"Premium is not activated and premium commands can't be executed in the server.", color=0xB8B8B8)
			e.set_author(name="Numix Premium", icon_url=deactivated_premium)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			return await ctx.send(embed=e)

		elif trf == "True":
			e = discord.Embed(timestamp=ctx.message.created_at, description=f"Premium activated and all premium commands are unlocked and accessable in the server.", color=242424)
			e.set_author(name="Numix Premium", icon_url=activated_premium)
			e.set_footer(text="Numix Premium", icon_url=self.config.logo)
			return await ctx.send(embed=e)
		else:
			e = discord.Embed(timestamp=ctx.message.created_at, description=f"Premium is not activated and premium commands can't be executed in the server.", color=0xB8B8B8)
			e.set_author(name="Numix Premium", icon_url=deactivated_premium)
			e.set_footer(text="Numix", icon_url=self.config.logo)
			return await ctx.send(embed=e)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!report <member> <reason>", description="Reports a user to the staff members", name="report")
	async def report(self, ctx, member: discord.Member = None, *, reason = None):
		cluster = MongoClient(f"{self.config.mongo1}DataBase_1{self.config.mongo2}")
		collection = cluster.DataBase_1.settings
		MONGO_GUILD_SETTINGS = collection.find_one({ "_id": member.guild.id })
		ReportChannel = self.bot.get_channel(MONGO_GUILD_SETTINGS["report"])
		channel = ctx.message.channel
		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_author(name="Member Reported", icon_url=ctx.author.avatar_url)
		embed.add_field(name="Reported User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)", inline = False)
		embed.add_field(name="Reported By:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inline = False)
		embed.add_field(name="Reason:", value=f"{reason}", inline = False)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text="Numix", icon_url=self.config.logo)

		if member is None:
			await ctx.send(f"{self.config.forbidden} speficy a user.")
		elif reason is None:
			await ctx.send(f"{self.config.forbidden} speficy a reason.")
		else:
			await ReportChannel.send(embed=embed)
			await channel.send(f"{self.config.success} This member has been reported.")
	
	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!avatar [member]", description="Shows the avatar of a mentioned user.", aliases=["av"])
	async def avatar(self, ctx, member: discord.User = None):
		if member is None:
			member = ctx.message.author
		else:
			pass
		a = member.avatar_url
		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_author(name=f"{member.name}#{member.discriminator}'s avatar", icon_url=f"{a}")
		embed.set_image(url=f"{a}")
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!links", description="Shows all the links related to Numix.", aliases=["inv", "invite", "link", "ss", "support", "supportserver"])
	async def links(self, ctx):
		embed = discord.Embed(timestamp=ctx.message.created_at, description=f"{self.config.arrow} **Website Link:** https://numix.xyz\n{self.config.arrow} **Bot Invite:** https://numix.xyz/invite\n{self.config.arrow} **Support Server:** https://numix.xyz/discord\n{self.config.arrow} **Minecraft Discord:** https://numix.xyz/mc\n\nThis bot is made, managed, and maintained by **{self.config.devs}**", color=242424)
		embed.set_author(name="Numix Related Links", icon_url=self.config.logo)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)
	
	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!about", description="Gives information about Numix.", aliases=["info", "dev", "stat", "stats", "ver", "version"])
	async def about(self,ctx):

		before = time.monotonic()
		before_ws = int(round(self.bot.latency * 1000, 1))
		embed = discord.Embed(timestamp=ctx.message.created_at, description="Hello there! I'm a unique and simple Discord bot, with various features. You will be able to see more about me in 5 seconds, You can always look at my commands and features with `n!help`.", colour=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		embed.set_author(name="Numix Quick Info", icon_url=self.config.logo)
		embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/6ZaNzxocvA0LBs_7spxKpNSU8dGqsmKyApoDFnvdF0E/https/cdn.discordapp.com/emojis/855604380571795487.gif?width=76&height=76")
		msg = await ctx.send(embed=embed)
		await asyncio.sleep(5)
		
		ping = (time.monotonic() - before) * 1000
		
		ram = self.process.memory_full_info().rss / 1024**2

		embed = discord.Embed(timestamp=ctx.message.created_at, description=f"[`Support`](https://numix.xyz/discord) • [`Invite`](https://numix.xyz/invite) • [`Vote`](https://top.gg/bot/744865990810271785)`\n\n<:dev:877394314433531947> **Developer:** {self.config.devs}\n<:version:877394315045924864> **Bot Version:** `{self.config.botversion}`\n<:speed:877394314781655061> **Ping:** `REST: {round(self.bot.latency * 1000)} | WS: {round(ping)}`\n<:commands:877400920705617921> **Loaded Commands:** `{len([x.name for x in self.bot.commands])}`\n<:folder:877402950077657218> **Lines of Code:** `Loading...`\n<:server:877394314651652127> **Servers:** `{len(self.bot.guilds)}`\n<:members:877398159368814623> **Total Members:** `{len(self.bot.users)}`", color=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		embed.set_author(name="Information about Numix", icon_url=self.config.logo)
		await msg.edit(content="", embed=embed)

		try:
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"[`Support`](https://numix.xyz/discord) • [`Invite`](https://numix.xyz/invite) • [`Vote`](https://top.gg/bot/744865990810271785)\n\n<:dev:877394314433531947> **Developer:** {self.config.devs}\n<:version:877394315045924864> **Bot Version:** `{self.config.botversion}`\n<:speed:877394314781655061> **Ping:** `REST: {round(self.bot.latency * 1000)} | WS: {round(ping)}`\n<:commands:877400920705617921> **Loaded Commands:** `{len([x.name for x in self.bot.commands])}`\n<:folder:877402950077657218> **Lines of Code:** `{countlines('/root/Numix')}` lines\n<:server:877394314651652127> **Servers:** `{len(self.bot.guilds)}`\n<:members:877398159368814623> **Total Members:** `{len(self.bot.users)}`", color=242424)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			embed.set_author(name="Information about Numix", icon_url=self.config.logo)
			await msg.edit(content="", embed=embed)
		except Exception:
			embed = discord.Embed(timestamp=ctx.message.created_at, description=f"[`Support`](https://numix.xyz/discord) • [`Invite`](https://numix.xyz/invite) • [`Vote`](https://top.gg/bot/744865990810271785)\n\n<:dev:877394314433531947> **Developer:** {self.config.devs}\n<:version:877394315045924864> **Bot Version:** `{self.config.botversion}`\n<:speed:877394314781655061> **Ping:** `REST: {round(self.bot.latency * 1000)} | WS: {round(ping)}`\n<:commands:877400920705617921> **Loaded Commands:** `{len([x.name for x in self.bot.commands])}`\n<:folder:877402950077657218> **Lines of Code:** `Internal Error`\n<:server:877394314651652127> **Servers:** `{len(self.bot.guilds)}`\n<:members:877398159368814623> **Total Members:** `{len(self.bot.users)}`", color=242424)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			embed.set_author(name="Information about Numix", icon_url=self.config.logo)
			await msg.edit(content="", embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!serverinfo", description="Gives informaiton about the server.", aliases=["server", "srvinfo"])
	@commands.bot_has_permissions(embed_links=True)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def serverinfo(self, ctx):
		role_count = len(ctx.guild.roles)
		txt_count = len(ctx.guild.text_channels)
		voice_count = len(ctx.guild.voice_channels)
		category_count = len(ctx.guild.categories)
		info1 = []
		features1 = set(ctx.guild.region)
		all_features1 = {
			'amsterdam': '🇳🇱 Amsterdam',
			'brazil': '🇧🇷 Brazil',
			'dubai': '🇦🇪 Dubai',
			'eu_central': '🇪🇺 Central Europe',
			'eu_west': '🇪🇺 West Europe',
			'europe': '🇪🇺 Europe',
			'frankfurt': '🇩🇪 Frankfurt',
			'hongkong': '🇭🇰 HongKong',
			'india': '🇮🇳 India',
			'japan': '🇯🇵 Japan',
			'london': '🇬🇧 London',
			'russia': '🇷🇺 Russia',
			'singapore': '🇸🇬 Singapore',
			'south_korea': '🇰🇷 South Korea',
			'sydney': '🇦🇺 Sydney',
			'us_central': '🇺🇸 US Central',
			'us_east': '🇺🇸 US East',
			'us_south': '🇺🇸 US South',
			'us_west': '🇺🇸 US West',
			'southafrica': '🇿🇦 South Africa'
		}

		for feature1, label1 in all_features1.items():
			if feature1 in features1:
				info1.append(f'{label1}')
		okay = ''.join(info1)
		region = okay
		info2 = []
		features2 = set(ctx.guild.verification_level)
		all_features2 = {
			'none': 'None',
			'low': 'Low',
			'medium': 'Medium',
			'high': 'High',
			'table_flip': 'High',
			'extreme': 'Extreme',
			'double_table_flip': 'Extreme',
			'very_high': 'Extreme'
		}
		for feature2, label2 in all_features2.items():
			if feature2 in features2:
				info2.append(f'{label2}')
		okay2 = ''.join(info2)
		verify = okay2
		if ctx.guild.rules_channel is not None:
			rules = ctx.guild.rules_channel.mention
		else:
			rules = "Not Set."

		if ctx.guild.system_channel is not None:
			system = ctx.guild.system_channel.mention
		else:
			system = "Not Set."

		if	ctx.guild.afk_channel is not None:
			afk = ctx.guild.afk_channel.mention
			afk_timer = f"{int(ctx.guild.afk_timeout/60)} Minutes"
		else:
			afk = "Not Set."
			afk_timer = "Not Set."

		stage_count = len(ctx.guild.stage_channels)


		if ctx.guild.premium_tier != 0:
			Level = f'<:right_arrow:877884586678419507> **Boosts Level:** {ctx.guild.premium_tier}'
			Boosts = f'<:right_arrow:877884586678419507> **Server Boosts:** {ctx.guild.premium_subscription_count}'

			last_boost = max(ctx.guild.members, key=lambda m: m.premium_since or ctx.guild.created_at)
			if last_boost.premium_since is not None:
				Last = f'<:right_arrow:877884586678419507> **Last Booster:** `{last_boost}` {format_relative(last_boost.premium_since)}'
			else:
				Last = ""
		else:
			Level = " "
			Boosts = " "
			Last = ""
			
		embed2 = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed2.set_author(name=f"{ctx.guild.name} Info", icon_url=ctx.guild.icon_url)


		emoji_stats = Counter()
		for emoji in ctx.guild.emojis:
			if emoji.animated:
				emoji_stats['animated'] += 1
				emoji_stats['animated_disabled'] += not emoji.available
			else:
				emoji_stats['regular'] += 1
				emoji_stats['disabled'] += not emoji.available

		fmt = f'<:right_arrow:877884586678419507> **Regular:** {emoji_stats["regular"]}/{ctx.guild.emoji_limit}\n' \
				f'<:right_arrow:877884586678419507> **Animated:** {emoji_stats["animated"]}/{ctx.guild.emoji_limit}\n' \

		if emoji_stats['disabled'] or emoji_stats['animated_disabled']:
			fmt = f'{fmt}**Disabled:** {emoji_stats["disabled"]} regular, {emoji_stats["animated_disabled"]} animated.'

		fmt = f'{fmt}<:right_arrow:877884586678419507> **Total Emoji:** {len(ctx.guild.emojis)}/{ctx.guild.emoji_limit*2}'


		embed2.add_field(name = "General information", value = f"""
		<:right_arrow:877884586678419507> **Server Name**: {ctx.guild.name}
		<:right_arrow:877884586678419507> **Server Owner**: {ctx.guild.owner.mention}
		<:right_arrow:877884586678419507> **Server Region**: {region}
		<:right_arrow:877884586678419507> **Verification Level**: {verify}
		<:right_arrow:877884586678419507> **Rules Channel**: {rules}
		<:right_arrow:877884586678419507> **System Channel**: {system}
		<:right_arrow:877884586678419507> **AFK Channel**: {afk}
		<:right_arrow:877884586678419507> **AFK Timer**: {afk_timer}
		""", inline=True)

		embed2.add_field(name = "Statistics", value = f"""
		<:right_arrow:877884586678419507> **Server Members**: {ctx.guild.member_count} Members
		<:right_arrow:877884586678419507> **Server Bots**: {sum(m.bot for m in ctx.guild.members)} Bots
		<:right_arrow:877884586678419507> **Server Roles**: {str(role_count)} Roles
		<:right_arrow:877884586678419507> **Server Categories**: {(category_count)} Categories
		<:right_arrow:877884586678419507> **Text Channels**: {txt_count} Channels
		<:right_arrow:877884586678419507> **Voice Channels**: {voice_count} Channels
		<:right_arrow:877884586678419507> **Stage Channels**: {stage_count} Channels
		""", inline=True)
		embed2.add_field(name = "Other information", value = f"""
		<:right_arrow:877884586678419507> **Online Members**: {sum(member.status==discord.Status.online and not member.bot for member in ctx.message.guild.members)}
		<:right_arrow:877884586678419507> **Offline Members**: {sum(member.status==discord.Status.offline and not member.bot for member in ctx.message.guild.members)}
		<:right_arrow:877884586678419507> **Idle Members**: {sum(member.status==discord.Status.idle and not member.bot for member in ctx.message.guild.members)}
		<:right_arrow:877884586678419507> **DND Members**: {sum(member.status==discord.Status.dnd and not member.bot for member in ctx.message.guild.members)}
		{Level}
		{Boosts}
		{Last}
		{fmt}
		""", inline=False)
		info = []
		features = set(ctx.guild.features)
		all_features = {
			'PARTNERED': 'Partnered',
			'VERIFIED': 'Verified',
			'DISCOVERABLE': 'Server Discovery',
			'COMMUNITY': 'Community Server',
			'FEATURABLE': 'Featured',
			'WELCOME_SCREEN_ENABLED': 'Welcome Screen',
			'INVITE_SPLASH': 'Invite Splash',
			'VIP_REGIONS': 'VIP Voice Servers',
			'VANITY_URL': 'Vanity Invite',
			'COMMERCE': 'Commerce',
			'LURKABLE': 'Lurkable',
			'NEWS': 'News Channels',
			'ANIMATED_ICON': 'Animated Icon',
			'BANNER': 'Banner'
		}

		for feature, label in all_features.items():
			if feature in features:
				MONGO = MongoClient(f"{self.config.db1}")
				premium_collection = MONGO.DataBase_1.premium
				if "Numix Premium" not in info:
					if premium_collection.count_documents({ "_id": f"{ctx.guild.id}", "premium": "True" }) == 1:
						info.append(f"**<:verified:877850058345820171>:** Numix Premium")
				info.append(f'**<:verified:877850058345820171>:** {label}')

		if info:
			embed2.add_field(name='Features', value='\n'.join(info), inline=True)

		embed2.set_thumbnail(url=ctx.guild.icon_url)

		embed2.set_footer(text='Numix | Created at ', icon_url=self.config.logo).timestamp = ctx.guild.created_at

		await ctx.send(embed=embed2)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!lookup [member]", description=f"Lookup information about the user.")
	@permission("manage_messages")
	async def lookup(self, ctx, user: discord.Member = None):
		if user is None:
			user = ctx.message.author
		try:
			game = user.activities[-1].name
			if game == "Spotify":
				game = f"[Spotify](https://open.spotify.com/track/{user.activities[0].track_id})"
		except:
			game = None
		
		voice_state = None if not user.voice else user.voice.channel
		embed = discord.Embed(timestamp=ctx.message.created_at, description=f"{self.config.ref_buttons}\n\n{self.config.arrow} **User:** {user.name}#{user.discriminator}(`{user.id}`)", colour=242424)
		
		embed.add_field(name='**Server-Side Info**', value=f"{self.config.arrow} **Nick:** `{user.nick}`\n{self.config.arrow} **In Voice:** {voice_state}\n{self.config.arrow} **Highest Role:** <@&{user.top_role.id}>\n{self.config.arrow} **Joined Date:** `{user.joined_at.__format__('%A, %d. %B %Y')}`\n{self.config.arrow} **Joined Time:** `{user.joined_at.__format__('%H:%M:%S')}`", inline=False)
		
		embed.add_field(name='**Account-Side Info**', value=f"{self.config.arrow} **Numix Badges:** {badges(self, ctx.author.id)}\n{self.config.arrow} **Status:** {user.status}\n{self.config.arrow} **Game/Custom Status:** {game}\n{self.config.arrow} **On Mobile:** `{user.is_on_mobile()}`\n{self.config.arrow} **Bot User:** `{user.bot}`\n{self.config.arrow} **Account Creation Date:** `{user.created_at.__format__('%A, %d. %B %Y')}`\n{self.config.arrow} **Account Creation Time:** `{user.created_at.__format__('%H:%M:%S')}`", inline=False)

		embed.set_author(name=user.name, icon_url=user.avatar_url)
		embed.set_footer(text='Numix', icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!status [member]", description="Check what a user is listening to.", aliases=["game", "cs", "custom-status", "customstatus"])
	async def status(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		game = member.activities[-1].name
		if game == "Spotify":
			await ctx.send(f"https://open.spotify.com/track/{member.activities[-1].track_id}")

		elif game == "Straming":
			embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			embed.set_author(name=f"{member} is Streaming on twitch", icon_url=member.avatar_url)
			embed.add_field(name="Stream Title:", value=f"{game.title}")
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)
		
		else:
			return await ctx.send(f"{self.config.forbidden} User is not listening to any spotify track currently or have a custom status.")

def setup(bot):
	bot.add_cog(general(bot))