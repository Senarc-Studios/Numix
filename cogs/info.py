from numix_imports import *
import motor.motor_asyncio

config = default.get('./config.json')

MONGO = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"
cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGO)
leveling = cluster["DataBase_1"]['Leveling']

class CustomCommand(commands.Command):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.perms = kwargs.get("perms", None)
		self.syntax = kwargs.get("syntax", None)

def countlines(rootdir, total_lines=0, header=True, begin_start=None, code_only=True):
	def _get_new_lines(source):
		total = len(source)
		i = 0
		while i < len(source):
			line = source[i]
			trimline = line.lstrip(" ")

			if trimline.startswith('#') or trimline == '':
				total -= 1
			elif '"""' in trimline:  # docstring begin
				if trimline.count('"""') == 2:  # docstring end on same line
					total -= 1
					i += 1
					continue
				doc_start = i
				i += 1
				while '"""' not in source[i]:  # docstring end
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
			total_lines = countlines(file, total_lines, header=False,
									 begin_start=rootdir, code_only=code_only)
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

	# @commands.command(cls=CustomCommand, perms="@everyone", syntax="n!skin", description="Gets a Minecraft Skin of a player.", aliases=[ "mc-skin" ])
	# async def skin(self, ctx, username=None):
	# 	if username == None:
	# 		return await ctx.send(f"{self.config.forbidden} Specify a Username to get the skin.")
	# 	embed = discord.Embed(timestamp=ctx.message.created_at, colour=242424)
	# 	embed.set_image(url="https://")

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

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!serverinfo", description="Shows information about the server.", aliases=["server-info", "server"])
	async def serverinfo(self, ctx):

		default_notification_setting = f"{ctx.guild.default_notifications}"
		default_notification_converter = default_notification_setting.replace("NotificationLevel.only_mentions", "Only @mentions")
		default_notification = default_notification_converter.replace("NotificationLevel.all_messages", "All Messages")
		owner = get(self.bot.users, id=ctx.guild.owner_id)

		date_1 = f"{ctx.guild.created_at.__format__('%d-%B-%Y @ %H:%M:%S')}"
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
		creation_date = date_13

		if ctx.guild.mfa_level == 0:

			guild = ctx.guild
			e = sum([1 for m in ctx.guild.members if m.bot])
			humans = sum(not member.bot for member in ctx.guild.members)
			embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
			embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
			embed.add_field(name="Server Region:", value=f"`{ctx.guild.region}`", inline=False)
			embed.add_field(name="Owner:", value=f"{owner.name}#{owner.discriminator}(`{owner.id}`)", inline=True)
			embed.add_field(name = "Server ID:", value=f"`{ctx.guild.id}`", inline=False)
			embed.add_field(name="Verification Level:", value=f"`{ctx.guild.verification_level}`", inline=True)
			embed.add_field(name="2FA requirement for mods:", value=f"`Disabled`", inline=False)
			embed.add_field(name="Default Notification Level:", value=f"`{default_notification}`", inline=True)
			embed.add_field(name="Boosts:", value=f"`{(ctx.guild.premium_subscription_count)}`", inline=False)
			embed.add_field(name="Boost Tier:", value=f"`{ctx.guild.premium_tier}`", inline=True)
			embed.add_field(name="Guild Creation Time:", value=f"`{creation_date}`", inline=False)
			embed.add_field(name="Total Members:", value=f"`{ctx.guild.member_count}`", inline=True)
			embed.add_field(name="Bots:", value=f"`{e}`", inline=False)
			embed.add_field(name="Humans:", value=f"`{humans}`", inline=True)
			embed.add_field(name="Roles:", value=f"`{len(ctx.guild.roles)}`", inline=False)
			embed.add_field(name="Voice Channels:", value=f"`{len(guild.voice_channels)}`", inline=True)
			embed.add_field(name="Text Channels:", value=f"`{len(guild.text_channels)}`", inline=False)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)

		elif ctx.guild.mfa_level == 1:
			
			guild = ctx.guild
			e = sum([1 for m in ctx.guild.members if m.bot])
			humans = sum(not member.bot for member in ctx.guild.members)
			embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
			embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
			embed.add_field(name="Server Region:", value=f"`{ctx.guild.region}`", inline=False)
			embed.add_field(name="Owner:", value=f"{owner.name}#{owner.discriminator}(`{owner.id}`)", inline=True)
			embed.add_field(name = "Server ID:", value=f"`{ctx.guild.id}`", inline=False)
			embed.add_field(name="Verification Level:", value=f"**{ctx.guild.verification_level}**", inline=True)
			embed.add_field(name="Server 2FA:", value=f"Enabled", inline=False)
			embed.add_field(name="Default Notification Level:", value=f"{default_notification}", inline=True)
			embed.add_field(name="Boosts:", value=f"`{(ctx.guild.premium_subscription_count)}`", inline=False)
			embed.add_field(name="Boost Tier:", value=f"`{ctx.guild.premium_tier}`", inline=True)
			embed.add_field(name="Guild Creation Time:", value=f"`{creation_date}`", inline=False)
			embed.add_field(name="Total Members:", value=f"`{ctx.guild.member_count}`", inline=True)
			embed.add_field(name="Bots:", value=f"`{e}`", inline=False)
			embed.add_field(name="Humans:", value=f"`{humans}`", inline=True)
			embed.add_field(name="Roles:", value=f"`{len(ctx.guild.roles)}`", inline=False)
			embed.add_field(name="Voice Channels:", value=f"`{len(guild.voice_channels)}`", inline=True)
			embed.add_field(name="Text Channels:", value=f"`{len(guild.text_channels)}`", inline=False)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)
	
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
		embed = discord.Embed(timestamp=ctx.message.created_at, description=f"**Website Link:** https://numix.xyz\n**Bot Invite:** https://numix.xyz/invite\n**Support Server:** https://numix.xyz/discord\n**Minecraft Discord:** https://numix.xyz/mc\n\nThis bot is made, managed, and maintained by **{self.config.devs}**", color=242424)
		embed.set_author(name="Numix Related Links", icon_url=self.config.logo)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)
	
	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!about", description="Gives information about Numix.", aliases=["info", "dev", "stat", "stats", "ver", "version"])
	async def about(self,ctx):

		before = time.monotonic()
		before_ws = int(round(self.bot.latency * 1000, 1))
		await ctx.send("Testing ping...", delete_after=0)
		ping = (time.monotonic() - before) * 1000

		ram = self.process.memory_full_info().rss / 1024**2
		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		embed.set_author(name="Numix Bot", icon_url=self.config.logo)
		embed.add_field(name="Developers:", value=f"{self.config.devs}", inline=False)
		embed.add_field(name="Bot Version:", value=f"{self.config.botversion}", inline=False)
		embed.add_field(name="Ping:", value=f"WS: `{before_ws}`ms | REST: `{int(ping)}`ms")
		embed.add_field(name="Support Server:", value=f"{self.config.supportserver}", inline=False)
		embed.add_field(name="Invited Servers:", value=f"`{len(self.bot.guilds)}` Servers", inline=False)
		embed.add_field(name="All Members:", value=f"`{len(self.bot.users)}` Members", inline=False)
		embed.add_field(name="Loaded Commands:", value=len([x.name for x in self.bot.commands]), inline=False)
		embed.add_field(name="Numix Code Lines:", value=f"`{countlines('/root/Numix')}` lines")
		embed.add_field(name="Ram Usage:", value=f"{ram} MB", inline=False)
		await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!lookup [member]", description="Lookup information about the user.")
	@commands.has_permissions(manage_messages=True)
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
		embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
		embed.add_field(name='User:', value=f"{user.name}#{user.discriminator}(`{user.id}`)", inline=False)
		embed.add_field(name='Nick:', value=user.nick, inline=False)
		embed.add_field(name='Status:', value=user.status, inline=False)
		embed.add_field(name='On Mobile:', value=user.is_on_mobile(), inline=False)
		embed.add_field(name='In Voice:', value=voice_state, inline=False)
		embed.add_field(name='Game / Custom Status:', value=game, inline=False)
		embed.add_field(name='Highest Role:', value=user.top_role.name, inline=False)
		embed.add_field(name="Bot User:", value=f"{user.bot}", inline=False)
		embed.add_field(name='Account Created Date:', value=user.created_at.__format__('%A, %d. %B %Y'), inline=False)
		embed.add_field(name='Account Creation Time:', value=user.created_at.__format__('%H:%M:%S'), inline=False)
		embed.add_field(name='Join Date:', value=user.joined_at.__format__('%A, %d. %B %Y'), inline=False)
		embed.add_field(name='Joined Time:', value=user.joined_at.__format__('%H:%M:%S'), inline=False)
		embed.set_author(name=user.name, icon_url=user.avatar_url)
		embed.set_footer(text='Numix', icon_url=self.config.logo)
		await ctx.send(embed=embed)

		"""
		<Activity type=<ActivityType.watching: 3> name='YouTube Together' url=None details="SIMPLE ROBINSON'S BEST OF DISCORD 2020" application_id=755600276941176913 session_id='5f49cf1e7ec4999e2067f2eb44b2f3f5' emoji=None>
		"""

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