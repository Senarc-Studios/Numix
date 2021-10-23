"""
BSD 3-Clause License

Copyright (c) 2021-present, BenitzCoding
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from numix_imports import *
import datetime
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='[%H:%M:%S]: ')

# Define Cogs

config = default.get("config.json")

class Logs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = config
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		logging.info(f"Numix was added to \"{guild.name}\"")
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
		logging.info(f"Numix was removed from \"{guild.name}\"")
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
		logging.info(f"{member.name} has joined guild \"{member.guild.name}\"")
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
		logging.info(f"{member.name} has left guild \"{member.guild.name}\"")
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
		logging.info(f"A message was deleted in \"{message.guild.name}\"")
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
		logging.info(f"A message was edited in \"{a.guild.name}\"")
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