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
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='[%H:%M:%S]: ')

debug = "debug"
python = "python"
html = "html"
css = "css"
js = "js"
java = "java"
json = "json"

class Debug(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")

	async def log(self, mode, content):
		try:
			print(content)
			string = ""
			if mode == "debug":
				string = f"```diff\n{content}\n```"

			elif mode == "python":
				string = f"```py\n{content}\n```"

			elif mode == "html":
				string = f"```html\n{content}\n```"

			elif mode == "css":
				string = f"```css\n{content}\n```"

			elif mode == "js":
				string = f"```js\n{content}\n```"

			elif mode == "java":
				string = f"```java\n{content}\n```"

			elif mode == "json":
				string = f"```json\n{content}\n```"
			
			else:
				string = content

			channel = await self.bot.fetch_channel(self.config.debug_channel)

			embed = discord.Embed(description=string, color=242424)
			embed.set_author(name="Debug Mode", icon_url=self.config.logo)
			embed.set_footer(text="Numix Developers", icon_url=self.config.logo)
			await channel.send(embed=embed)

			return True
		
		except:
			logging.log(f"An error occured while sending the Debug message.")
			return False

	@commands.Cog.listener()
	async def on_ready(self):
		logging.info(f"Numix is ready.")
		await self.log(mode=debug, content="+ Bot Booted with Debug Enabled.")

	@commands.Cog.listener()
	async def on_command(self, ctx):
		logging.info(f"{ctx.author.name} used the {ctx.command} Command.")
		await self.log(mode=python, content=f"[{ctx.command}]:\n"+"{\n"+f"  \"ctx\": {ctx},\n  \"name\": \"{ctx.author.name}\",\n  \"discriminator\": {ctx.author.discriminator},\n  \"author-id\": {ctx.author.id},\n \"message-id\": {ctx.message.id},\n \"bot\": {ctx.author.bot},\n \"guild\": \"{ctx.guild.name}\",\n \"guild-id\": {ctx.guild.id}\n" + "}")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild == None:
			logging.info(f"{message.author.name} Direct Messaged \"{message.content}\"")
			await self.log(mode=json, content=("{" + f"\n  \"name\": \"{message.author.name}\",\n  \"discriminator\": {message.author.discriminator},\n  \"author-id\": {message.author.id},\n  \"message-id\": {message.id},\n  \"bot\": {message.author.bot},\n  \"message-content\": \"{message.content}\"\n" + "}"))

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		await self.log(mode=python, content=f"[{ctx.command}]: {error}")

def setup(bot):
	bot.add_cog(Debug(bot))