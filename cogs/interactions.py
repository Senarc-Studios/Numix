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

class Interactions(commands.Cog):
	def __init__(self, bot):
		print("\"Interactions\" cog loaded")
		self.bot = bot
		self.config = default.get("./config.json")
		self.MONGO_CONNECTION = MongoClient(f"{self.config.db1}")
		self.MONGO = self.MONGO_CONNECTION.DataBase_1.interactions

	@commands.Cog.listener()
	async def on_command(self, ctx):
		if self.MONGO.count_documents({ "_id": ctx.command.name }) == 0:
			return self.MONGO.insert_one({ "_id": ctx.command.name, "uses": 1 })

		else:
			for data in self.MONGO.find({ "_id": ctx.command.name }):
				self.MONGO.update_one({ "_id": ctx.command.name }, { "$set": { "_id": ctx.command.name, "uses": data["uses"] + 1 } })
			
				for fdata in self.MONGO.find({ "_id": "all" }):
					self.MONGO.update_one({ "_id": "all" }, { "$set": { "_id": "all", "uses": fdata["uses"] + 1 } })

					guild = discord.utils.get(self.bot.guilds, id=self.config.supportserver)
					channel = discord.utils.get(guild.text_channels, id=self.config.interaction_log)
					server_owner = discord.utils.get(self.bot.users, id=ctx.guild.owner_id)
					embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
					embed.set_author(name=f"{ctx.author.name} used {ctx.command.name}", icon_url=ctx.author.display_avatar)
					embed.add_field(name="Guild ID:", value=f"{ctx.guild.name}(`{ctx.guild.id}`)")
					embed.add_field(name="Guild Owner", value=f"{server_owner.name}#{server_owner.discriminator}(`{server_owner.id}`)", inline=False)
					embed.add_field(name="Member:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inline=False)
					embed.add_field(name="Global Command Uses:", value=f"{data['uses']+1}", inline=False)
					embed.add_field(name="All Global Command Uses:", value=f"{fdata['uses']+1}", inline=False)
					embed.set_footer(text="Numix Data Sector", icon_url=self.config.logo)
					await channel.send(embed=embed)

async def setup(bot):
	await bot.add_cog(Interactions(bot))