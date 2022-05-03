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

class ADS_Plugin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")

	@commands.Cog.listener()
	async def on_ready(self):
		blocked_users = self.config.ads
		for guild in self.bot.guilds:
			if guild.owner_id in blocked_users:
				await guild.leave()
				ss = get(self.bot.guilds, id=791553406266245121)
				log = get(ss.text_channels, id=791556611951820801)
				await log.send(f":no_entry_sign: Blocked Server by **Anti-Dummy Server** Module, **Server_Name:** {guild.name}, **Server_ID:** {guild.id}")
		print("ADS Script Ended after on_ready.")

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		if guild.owner_id in self.config.ads:
			await guild.leave()
			ss = get(self.bot.guilds, id=791553406266245121)
			log = get(ss.text_channels, id=791556611951820801)
			await log.send(f":no_entry_sign: Blocked Server by **Anti-Dummy Server** Module, **Server_Name:** {guild.name}, **Server_ID:** {guild.id}")
		else:
			return

	@commands.command(hidden=True, aliases=["run ads"])
	@commands.is_owner()
	async def run_ads(self, ctx):
		blocked_users = self.config.ads
		for guild in self.bot.guilds:
			if guild.owner_id in blocked_users:
				await guild.leave()
				
				log = get(ss.text_channels, id=791556611951820801)
				await log.send(f":no_entry_sign: Blocked Server by **Anti-Dummy Server** Module, **Server_Name:** {guild.name}, **Server_ID:** {guild.id}")
		await ctx.send("ADS Script Ended.")

async def setup(bot):
	await bot.add_cog(ADS_Plugin(bot))