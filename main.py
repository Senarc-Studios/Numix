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
import os
import discord

import motor.motor_asyncio

from numix_imports import *
from cool_utils import Terminal
from discord.ext import commands

cluster = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
collection = cluster['DataBase_1']['prefixes']

os.system('ls -l; pip install profanity-filter')
os.system('ls -l; python -m spacy download en')

Terminal.display("Numix Starting...")

async def debug_check():
	collection = cluster['DataBase_1']['assets']
	return await collection.find_one({ "_id": "debug" })['value']

# Intents For Numix

intents = discord.Intents.all()
intents.members = True

# Define Cogs

config = default.get("config.json")

# Bot Decorator

async def get_prefix(bot, message):
	global client
	if not message.guild:
		return commands.when_mentioned_or("n!")(bot, message)
	prefix = "n!"
	prefix = await collection.find_one({"_id":message.guild.id})["prefix"]
	return commands.when_mentioned_or(prefix)(bot, message)

async def sync_application(self):
	await self.tree.sync()
	Terminal.display("Application Commands synced successfully.")

class Numix(commands.AutoSharededBot):
	async def __init__(self):
		super().__init__(command_prefix=await get_prefix, intents=intents)
		self.debug = await debug_check()

	async def start(self, *args, **kwargs):
		await super().start(*args, **kwargs)

	async def close(self):
		await super().close()

	async def setup_hook(self):
		for filename in os.listdir("./cogs"):
			if filename.startswith("debug"):
				if self.debug:
					name = filename[:-3]
					await bot.load_extension(f"cogs.{name}")
				else:
					continue
			if filename.endswith(".py"):
				name = filename[:-3]
				try:
					await bot.load_extension(f"cogs.{name}")
					Terminal.display(f"\"{name}\" Cog Loaded.")
				except Exception as error:
					Terminal.warn(f"Loading \"{name}\" cog threw: {error}")

		self.loop.create_task(sync_application(self))

bot = asyncio.run(Numix())
bot.remove_command("help")

async def is_owner(ctx):
	dev = [727365670395838626, 529499034495483926, 709310923130667012, 526711399137673232]
	if ctx.author.id in dev:
		return True
	else:
		await ctx.send(f"{config.forbidden} You can't use that command.")
		return False

@bot.command(hidden=True, aliases=["pull", "git-pull", "update"])
async def fetch(ctx):
	if await is_owner(ctx, ctx.author) == False:
		return
	os.system(f"ls -l; git pull Numix master")
	await ctx.send(f"{config.success} Fetched all updates and reloading.")
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			name = file[:-3]
			bot.reload_extension(f"cogs.{name}")

# Eval

@bot.command(name='e', hidden=True, aliases=["eval"])
@commands.check(is_owner)
async def _e(ctx, *, body=None):
	if ctx.author.id not in config.owners:
		return await ctx.send(f"{config.forbidden} **`ERROR 401`**")
	env = {
		'ctx': ctx,
		'channel': ctx.channel,
		'author': ctx.author,
		'guild': ctx.guild,
		'message': ctx.message,
		'source': inspect.getsource
	}

	env.update(globals())

	body = cleanup_code(body)
	stdout = io.StringIO()
	err = out = None

	to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

	def paginate(text: str):
		'''Simple generator that paginates text.'''
		last = 0
		pages = []
		for curr in range(0, len(text)):
			if curr % 1980 == 0:
				pages.append(text[last:curr])
				last = curr
				appd_index = curr
		if appd_index != len(text)-1:
			pages.append(text[last:curr])
		return list(filter(lambda a: a != '', pages))

	try:
		exec(to_compile, env)
	except Exception as e:
		err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
		return await ctx.message.add_reaction('\u2049')

	func = env['func']
	try:
		with redirect_stdout(stdout):
			ret = await func()
	except Exception as e:
		value = stdout.getvalue()
		err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
	else:
		value = stdout.getvalue()
		if ret is None:
			if value:
				try:

					out = await ctx.send(f'```py\n{value}\n```')
				except:
					paginated_text = paginate(value)
					for page in paginated_text:
						if page == paginated_text[-1]:
							out = await ctx.send(f'```py\n{page}\n```')
							break
						await ctx.send(f'```py\n{page}\n```')
		else:
			bot._last_result = ret
			try:
				out = await ctx.send(f'```py\n{value}{ret}\n```')
			except:
				paginated_text = paginate(f"{value}{ret}")
				for page in paginated_text:
					if page == paginated_text[-1]:
						out = await ctx.send(f'```py\n{page}\n```')
						break
					await ctx.send(f'```py\n{page}\n```')

	if out:
		await ctx.message.add_reaction('\u2705')  # tick
	elif err:
		await ctx.message.add_reaction('\u2049')  # x
	else:
		await ctx.message.add_reaction('\u2705')

def cleanup_code(content):
	"""Automatically removes code blocks from the code."""
	# remove ```py\n```
	if content.startswith('```') and content.endswith('```'):
		return '\n'.join(content.split('\n')[1:-1])

	# remove `foo`
	return content.strip('` \n')

def get_syntax_error(e):
	if e.text is None:
		return f'```py\n{e.__class__.__name__}: {e}\n```'
	return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

# Load Cog

@bot.command(hidden=True)
@commands.check(is_owner)
async def load(ctx, *, name: str):
	try:
		bot.load_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'"**{name}**" Cog loaded')

# Unload Cog

@bot.command(hidden=True)
@commands.check(is_owner)
async def unload(ctx, *, name: str):
	try:
		bot.unload_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'"**{name}**" Cog unloaded')

# Reload Cog

@bot.command(hidden=True)
@commands.check(is_owner)
async def reload(ctx, *, name: str):
	if name == "all":
		await ctx.send("**All** Cogs are reloaded.")
		for file in os.listdir("./cogs"):
			if file.endswith(".py"):
				name = file[:-3]
				bot.reload_extension(f"cogs.{name}")
	try:
		bot.reload_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'Cog "**`{name}`**" has been reloaded.')

@bot.command(hidden=True)
@commands.check(is_owner)
async def restart(ctx):
	await ctx.send(f"{config.success} Performing Complete Restart on Numix.")
	os.system("ls -l; python3 main.py")
	await bot.logout()

# main
def main():
	for file in os.listdir("./cogs"):
		try:
			if file.startswith("debug"):
				if debug_check() == True:
					name = file[:-3]
					bot.load_extension(f"cogs.{name}")
				else:
					continue
			if file.endswith(".py"):
				name = file[:-3]
				bot.load_extension(f"cogs.{name}")
				Terminal.display(f"Loaded '{name}' cog.")
		except Exception as e:
			print(e)
	bot.load_extension("jishaku")
	Terminal.display(f"Loaded '{name}' cog.")
	try:
		bot.run(config.token)
	except Exception as e:
		print(e)

main()