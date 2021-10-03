from numix_imports import *
import datetime

# Define Cogs

config = default.get("config.json")

class Logs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
		print('"Logs" cog loaded')
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		for channel in guild.text_channels:
			nubot = guild.me
			if channel.permissions_for(nubot).send_messages == True:
				embed = discord.Embed(description="Thank You for inviting **Numix**.\nDefault Prefix `n!`", color=242424)
				embed.set_author(name="Numix Bot", icon_url=self.config.logo)
				embed.add_field(name="Developers:", value=self.config.devs, inline=False)
				embed.add_field(name="Loaded Commands:", value=len([x.name for x in self.bot.commands]), inline=False)
				embed.add_field(name="All Servers:", value=f"`{len(self.bot.guilds)}` Servers", inline=False)
				embed.add_field(name="All Members:", value=f"`{len(self.bot.users)}` Members", inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await channel.send(embed=embed)
				
				link = await channel.create_invite(max_age = 0)
				support_server = get(self.bot.guilds, id=826709598953144330)
				join_log_channel = get(support_server.text_channels, id=877850492791836672)
				log_message = discord.Embed(color=242424)
				log_message.set_author(name=f"Joined {guild.name}", icon_url=guild.icon_url)
				log_message.add_field(name="Server ID:", value=f"{self.config.arrow} `{guild.id}`", inline=False)
				log_message.add_field(name="Owner's ID:", value=f"{self.config.arrow} `{guild.owner_id}`", inline=False)
				log_message.add_field(name="Owner Mention:", value=f"{self.config.arrow} <@!{guild.owner_id}>", inline=False)
				log_message.set_footer(text="Numix Developers", icon_url=self.config.logo)
				log_message.set_thumbnail(url=f"{guild.icon_url}")
				await join_log_channel.send(embed=log_message)
				return
			else:
				continue

	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		support_server = get(self.bot.guilds, id=826709598953144330)
		leave_log_channel = get(support_server.text_channels, id=877850532075700255)
		log_message = discord.Embed(color=242424)
		log_message.set_author(name=f"Left {guild.name}", icon_url=guild.icon_url)
		log_message.add_field(name="Server ID:", value=f"{self.config.arrow} `{guild.id}`", inline=False)
		log_message.add_field(name="Owner's ID:", value=f"{self.config.arrow} `{guild.owner_id}`", inline=False)
		log_message.add_field(name="Owner Mention:", value=f"{self.config.arrow} <@!{guild.owner_id}>", inline=False)
		log_message.set_footer(text="Numix Developers", icon_url=self.config.logo)
		log_message.set_thumbnail(url=guild.icon_url)
		await leave_log_channel.send(embed=log_message)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		try:

			cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
			collection = cluster.DataBase_1.settings

			for x in collection.find({"_id":int(member.guild.id)}):
				logid = x["log"]
				guild = get(self.bot.guilds, id=member.guild.id)
				log = get(guild.text_channels, id=int(logid))

				log_message = discord.Embed(timestamp=member.joined_at, color=242424)
				log_message.set_author(name=f"{member.name} Joined", icon_url=member.display_avatar)
				log_message.add_field(name="User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
				log_message.add_field(name='Account Creation:', value=member.created_at.__format__('%A, %d. %B %Y on %H:%M:%S'), inline=False)
				log_message.set_footer(text="Numix", icon_url=self.config.logo)
				await log.send(embed=log_message)
		except:
			pass

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		try:
			guild = member.guild
			cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
			collection = cluster.DataBase_1.settings

			for x in collection.find({"_id": guild.id}):
				logid = x["log"]
				guild = get(self.bot.guilds, id=guild.id)
				log = get(guild.text_channels, id=logid)

				log_message = discord.Embed(timestamp=datetime.datetime.utcnow(), color=242424)
				log_message.set_author(name=f"{member.name} Left", icon_url=member.display_avatar)
				log_message.add_field(name="User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
				log_message.add_field(name='Account Creation:', value=member.created_at.__format__('%A, %d. %B %Y on %H:%M:%S'), inline=False)
				log_message.add_field(name='Joined At:', value=member.joined_at.__format__('%A, %d. %B %Y on %H:%M:%S'), inline=False)
				log_message.set_footer(text="Numix", icon_url=self.config.logo)
				await log.send(embed=log_message)
		except:
			pass

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		try:

			cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
			collection = cluster.DataBase_1.settings

			for x in collection.find({"_id":message.guild.id}):
				logid = x["log"]
				guild = get(self.bot.guilds, id=message.guild.id)
				log = get(guild.text_channels, id=logid)


				if message.content == "":
					return

				else:
					embed = discord.Embed(timestamp=datetime.datetime.utcnow(), description=f'**Message Author:** \n<@!{message.author.id}>(`{message.author.id}`) \n\n**Message Channel:**\n<#{message.channel.id}> \n\n**Message Content:**\n```{message.content.replace("`", "")}```', color=242424)
					embed.set_author(name=f"Message Deleted", icon_url=message.author.display_avatar)
					embed.set_footer(text='Numix', icon_url=self.config.logo)
					await log.send(embed=embed)
		except:
			pass

	@commands.Cog.listener()
	async def on_message_edit(self, a, b):
		try:
			cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
			collection = cluster.DataBase_1.settings

			guild = get(self.bot.guilds, id=a.guild.id)

			for x in collection.find({"_id":guild.id}):
				logid = x["log"]
				guild = get(self.bot.guilds, id=guild.id)
				log = get(guild.text_channels, id=logid)

				if a.content == b.content + "":
					return

				elif b.content == "":
					return

				else:
					before = a.content.replace("`", "")
					after = b.content.replace("`", "")
					embed = discord.Embed(timestamp=a.created_at, description=f'**Message Author:** \n<@!{a.author.id}>(`{a.author.id}`) \n\n**Message Channel:**\n<#{a.channel.id}> \n\n**Before Edit:**```{before}```\n\n**After Edit:**```{after}```', color=242424)
					embed.set_author(name=f"Message Edited", icon_url=a.author.display_avatar)
					embed.set_footer(text='Numix', icon_url=self.config.logo)
					await log.send(embed=embed)
		except:
			pass

def setup(bot):
	bot.add_cog(Logs(bot))