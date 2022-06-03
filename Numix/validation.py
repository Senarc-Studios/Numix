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

config = default.get("./config.json")
mongo_DB1_url = f"{config.mongo1}DataBase_1{config.mongo2}"
db1 = MongoClient(mongo_DB1_url)

async def permission(self, ctx, permission, command):
	permission_ = permission.lower()

	if ctx.author.id in self.config.owners:
		return True
	
	elif ctx.message.author.guild_permissions.administrator:
		return True

	else:

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