from numix_imports import *

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

			channel = await self.bot.fetch_channel(880307133839712356)

			embed = discord.Embed(description=string, color=242424)
			embed.set_author(name="Debug Mode", icon_url=self.config.logo)
			embed.set_footer(text="Numix Developers", icon_url=self.config.logo)
			await channel.send(embed=embed)

			print("[Debug Message sent successfully.]")
			return True
		
		except:
			print("[An error occured while sending the Debug message.]")
			return False

	@commands.Cog.listener()
	async def on_ready(self):
		await self.log(mode=debug, content="+ Bot Booted with Debug Enabled.")

	@commands.Cog.listener()
	async def on_command(self, ctx):
		await self.log(mode=python, content=f"[{ctx.command.name}]: {ctx}")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild == None:
			await self.log(mode=json, content=("{" + f"\n  \"name\": \"{message.author.name}\",\n  \"discriminator\": {message.author.discriminator},\n  \"author-id\": {message.author.id},\n  \"message-id\": {message.id},\n  \"bot\": {message.author.bot},\n  \"message-content\": \"{message.content}\"\n" + "}"))

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		await self.log(mode=python, content=f"[{ctx.command.name}]: {error}")

def setup(bot):
	bot.add_cog(Debug(bot))