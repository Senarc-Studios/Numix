from numix_imports import *

# Define Cogs

config = default.get("config.json")

class Logs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
		print('"Logs" cog loaded')
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		support_server = get(self.bot.guilds, id=791553406266245121)
		join_log_channel = get(support_server.text_channels, id=791556611151626261)
		log_message = discord.Embed(title=f"Joined **{guild.name}**", color=242424)
		log_message.add_field(name="Server ID:", value=f"{guild.id}", inline=False)
		log_message.add_field(name="Owner's ID:", value=f"{guild.owner_id}", inline=False)
		log_message.add_field(name="Owner Mention:", value=f"<@!{guild.owner_id}>", inline=False)
		log_message.set_footer(text="Numix Developers", icon_url=self.config.logo)
		log_message.set_thumbnail(url=guild.avatar_url)
		await join_log_channel.send(embed=log_message)
		success = False
		i = 0
		while not success:
			try:
				embed = discord.Embed(description="Thank You for inviting **Numix**.\nDefault Prefix `n!`", color=242424)
				embed.set_author(name="Numix Bot", icon_url=self.config.logo)
				embed.add_field(name="Developers:", value=self.config.devs, inline=False)
				embed.add_field(name="Loaded Commands:", value=len([x.name for x in self.bot.commands]), inline=False)
				embed.add_field(name="All Servers:", value=f"`{len(self.bot.guilds)}` Servers", inline=False)
				embed.add_field(name="All Members:", value=f"`{len(self.bot.users)}` Members", inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await g.channels[i].send(embed=embed)
			except (discord.Forbidden, AttributeError):
				i += 1
			except IndexError:
				# if the server has no channels, doesn't let the bot talk, or all vc/categories
				pass
			else:
				success = True

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		support_server = get(self.bot.guilds, id=791553406266245121)
		leave_log_channel = get(support_server.text_channels, id=791556611151626261)
		log_message = discord.Embed(title=f"Joined **{guild.name}**", color=242424)
		log_message.add_field(name="Server ID:", value=f"{guild.id}", inline=False)
		log_message.add_field(name="Owner's ID:", value=f"{guild.owner_id}", inline=False)
		log_message.add_field(name="Owner Mention:", value=f"<@!{guild.owner_id}>", inline=False)
		log_message.set_footer(text="Numix Developers", icon_url=self.config.logo)
		log_message.set_thumbnail(url=guild.avatar_url)
		await leave_log_channel.send(embed=log_message)

	@commands.Cog.listener()
	async def on_member_join(self, member):

		cluster = MongoClient('mongodb+srv://Benitz:6vsdPiReMc2nTukr@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		for x in collection.find({"_id":int(member.guild.id)}):
			logid = x["log"]
			guild = get(self.bot.guilds, id=member.guild.id)
			log = get(guild.text_channels, id=int(logid))

			log_message = discord.Embed(timestamp=member.joined_at, color=242424)
			log_message.set_author(name=f"{member.name} Joined", icon_url=member.avatar_url)
			log_message.add_field(name="User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
			log_message.add_field(name='Account Creation:', value=member.created_at.__format__('%A, %d. %B %Y on %H:%M:%S'), inline=False)
			log_message.set_footer(text="Numix", icon_url=self.config.logo)
			await log.send(embed=log_message)

	@commands.Cog.listener()
	async def on_member_remove(self, member, guild):

		cluster = MongoClient('mongodb+srv://Benitz:6vsdPiReMc2nTukr@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		for x in collection.find({"_id":guild.id}):
			logid = x["log"]
			print(logid)
			guild = get(self.bot.guilds, id=guild.id)
			log = get(guild.text_channels, id=logid)

			log_message = discord.Embed(color=242424)
			log_message.set_author(name=f"{member.name} Left", icon_url=member.avatar_url)
			log_message.add_field(name="User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
			log_message.add_field(name='Account Creation:', value=member.created_at.__format__('%A, %d. %B %Y on %H:%M:%S'), inline=False)
			log_message.add_field(name='Joined At:', value=member.joined_at.__format__('%A, %d. %B %Y on %H:%M:%S'), inline=False)
			log_message.set_footer(text="Numix", icon_url=self.config.logo)
			await log.send(embed=log_message)

	@commands.Cog.listener()
	async def on_message_delete(self, message):

		cluster = MongoClient('mongodb+srv://Benitz:6vsdPiReMc2nTukr@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		for x in collection.find({"_id":message.guild.id}):
			logid = x["log"]
			print(logid)
			guild = get(self.bot.guilds, id=message.guild.id)
			log = get(guild.text_channels, id=logid)


			if message.content == "":
				return

			else:
				print(message.content)
				embed = discord.Embed(timestamp=message.created_at, description=f'**Message Author:** \n<@!{message.author.id}>(`{message.author.id}`) \n\n**Message Channel:**\n<#{message.channel.id}> \n\n**Message Content:**\n```{message.content}```', color=242424)
				embed.set_author(name=f"Message Deleted", icon_url=message.author.avatar_url)
				embed.set_footer(text='Numix', icon_url=self.config.logo)
				await log.send(embed=embed)

	@commands.Cog.listener()
	async def on_message_edit(self, a, b):
		cluster = MongoClient('mongodb+srv://Benitz:6vsdPiReMc2nTukr@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		guild = get(self.bot.guilds, id=a.guild.id)

		for x in collection.find({"_id":guild.id}):
			logid = x["log"]
			guild = get(self.bot.guilds, id=guild.id)
			log = get(guild.text_channels, id=logid)

			if a.content == b.content:
				return

			elif b.content == "":
				return

			else:
				embed = discord.Embed(timestamp=a.created_at, description=f'**Message Author:** \n<@!{a.author.id}>(`{a.author.id}`) \n\n**Message Channel:**\n<#{a.channel.id}> \n\n**Before Edit:**```{a.content}```\n\n**After Edit:**```{b.content}```', color=242424)
				embed.set_author(name=f"Message Edited", icon_url=a.author.avatar_url)
				embed.set_footer(text='Numix', icon_url=self.config.logo)
				await log.send(embed=embed)

def setup(bot):
	bot.add_cog(Logs(bot))