from numix_imports import *
import os
import discord
from discord.ext import commands

cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
collection = cluster.DataBase_1.prefixes

os.system('ls -l; pip install profanity-filter')
os.system('ls -l; python -m spacy download en')

print("Bot Starting.")

# Intents For Numix

intents = discord.Intents.default()
intents.members = True

# Define Cogs

config = default.get("config.json")

# Bot Decorator

def prefix(bot, message):
	global client
	if not message.guild:
		return commands.when_mentioned_or("n!")(bot, message)
	prefix = "n!"
	for x in collection.find({"_id":message.guild.id}):
		prefix=x["prefix"]
	return commands.when_mentioned_or(prefix)(bot, message)

bot = commands.AutoShardedBot(command_prefix=prefix, intents=intents)
bot.remove_command("help")

async def is_owner(self, user: discord.User):
	dev = [727365670395838626, 529499034495483926, 709310923130667012, 526711399137673232]
	if user.id in dev:  # Implement your own conditions here
		return True
	else:
		await ctx.send(f"{config.forbidden} You can't use that command.")
		return False


# Eval

@bot.command(name='e', aliases=["eval"])
@commands.is_owner()
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

@bot.command()
@commands.is_owner()
async def load(ctx, *, name: str):
	try:
		bot.load_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'"**{name}**" Cog loaded')

# Unload Cog

@bot.command()
@commands.is_owner()
async def unload(ctx, *, name: str):
	try:
		bot.unload_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'"**{name}**" Cog unloaded')

# Reload Cog

@bot.command()
@commands.is_owner()
async def reload(ctx, *, name: str):
	try:
		bot.reload_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'"**{name}**" Cog reloaded')

@bot.command()
@commands.is_owner()
async def restart(ctx):
	await ctx.send(f"{config.success} Performing Complete Restart on Numix.")
	os.system("ls -l; python3 main.py")
	await bot.logout()

# Read Cogs

for file in os.listdir("./cogs"):
	if file.endswith(".py"):
		name = file[:-3]
		bot.load_extension(f"cogs.{name}")


# Run Bot

try:
	bot.run(config.token, reconnect=True)
except Exception as e:
	print(e)
