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
from numix_log import *

class AntiNuker(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.Mongo_connection = MongoClient(self.config.db1)
		self.guild_bans = []
		self.guild_kicks = []
		self.guild_cd = []

	def basic_checks(self, guild):
		premium = self.db1.DataBase_1.premium

		premium_list = premium
		premium_validation_check = premium_list.count_documents({ "_id": f"{guild.id}" })

		if premium_validation_check == 0:
			return

		for guilds in premium.find({ "_id": f"{guild.id}" }):
			trf = guilds["premium"]
			trf = f"{trf}"

		if trf == "False":
			return "Fail"

		elif trf == "True":
			return "Pass"

		else:
			return "Fail"

	async def register_and_nukerban_check(self, guild, member):
		col = self.Mongo_collection.DataBase_1.nukeban
		logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
		logs = logs[0]
		if logs.reason == None:
			reason = "Unspecified"
		else:
			reason = logs.reason
		info = { "_id": guild.id, "banned_user": member.id, "moderator": logs.user.id, "reason": reason }
		col.insert_one(info)
		await log("ban", guild, member, logs.user, reason)

		if guild.id in self.guild_bans:
			try:
				for i in col.find({ "_id": f"{guild.id}_ban" }):
					count = i["ban_count"]
					col.update_one({ "_id": f"{guild.id}_ban" }, { "_id": f"{guild.id}_ban", "ban_count": count + 1 })
					if count >= 3:
						print("Anti-Nuker Executed")
						await guild.ban(log.user, reason=f"User was raiding the server.")
			except:
				count = 2
				col.insert_one({ "_id": f"{guild.id}_ban", "ban_count": count })

		self.guild_bans.append(guild.id)
		await asyncio.sleep(3)
		self.guild_bans.remove(guild.id)

	def check_toggle(self, guild):
		cluster = self.Mongo_connection
		collection = cluster.DataBase_1.settings
		for i in collection.find({ "_id": guild.id }):
			toggle = i["anuker"]
			if toggle == "False":
				return "False"
			if toggle == "True":
				return "True"
			else:
				return "False"

	async def register_and_nukerkick_check(self, guild, member):
		col = self.Mongo_collection.DataBase_1.nukekick
		logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
		logs = logs[0]
		if logs.reason == None:
			reason = "Unspecified"
		else:
			reason = logs.reason
		info = { "_id": guild.id, "kicked_user": member.id, "moderator": logs.user.id, "reason": reason }
		col.insert_one(info)
		await log("kick", guild, member, logs.user, reason)

		if guild.id in self.guild_kicks:
			try:
				for i in col.find({ "_id": f"{guild.id}_kick" }):
					count = i["kick_count"]
					col.update_one({ "_id": f"{guild.id}_kick" }, { "_id": f"{guild.id}_kick", "kick_count": count + 1 })
					if count >= 3:
						print("Anti-Nuker Executed")
						await guild.ban(log.user, reason=f"User was raiding the server.")
			except:
				count = 2
				col.insert_one({ "_id": f"{guild.id}_kick", "kick_count": count })

		self.guild_kicks.append(guild.id)
		await asyncio.sleep(3)
		self.guild_kick.remove(guild.id)

	async def register_and_nukerdelete_check(self, guild, channel):
		col = self.Mongo_collection.DataBase_1.nukedelete
		logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).flatten()
		info = { "_id": guild.id, "deleted_channel": channel.id, "moderator": logs.user.id }
		col.insert_one(info)
		await log("channel_delete", guild, channel, logs.user, None)

		if guild.id in self.guild_cd:
			try:
				for i in col.find({ "_id": f"{guild.id}cd" }):
					count = i["delete_count"]
					col.update_one({ "_id": f"{guild.id}_cd" }, { "_id": f"{guild.id}_cd", "delete_count": count + 1 })
					if count >= 3:
						print("Anti-Nuker Executed")
						await guild.ban(logs.user, reason=f"User was raiding the server.")
			except:
				count = 2
				col.insert_one({ "_id": f"{guild.id}_cd", "delete_count": count })

		self.guild_cd.append(guild.id)
		await asyncio.sleep(3)
		self.guild_cd.remove(guild.id)

	@commands.Cog.listener()
	async def on_member_ban(self, guild, member):
		self.check_toggle(guild)
		if self.basic_checks() == "Fail":
			return
		await self.register_and_nukerban_check(guild, member)

	@commands.Cog.listener()
	async def on_member_kick(self, guild, member):
		self.check_toggle(guild)
		if self.basic_checks() == "Fail":
			return
		await self.register_and_nukerkick_check(guild, member)

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		self.check_toggle(channel.guild)
		if self.basic_checks() == "Fail":
			return
		await self.register_and_nukerdelete_check(channel.guild, channel)

async def setup(bot):
	await bot.add_cog(AntiNuker(bot))