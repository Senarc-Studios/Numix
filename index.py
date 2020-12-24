from numix_imports import *

print("Bot Starting.")

# Intents

intents = discord.Intents.default()
intents.members = True

# Define Cogs

config = default.get("config.json")

# Bot Decorator

bot = commands.Bot(command_prefix=["N!", "n!", "Numix", "Numix ", "<@!545230136669241365>", "<@!545230136669241365> "], intents=intents)
bot.remove_command("help")

# Load Cog

@bot.command()
@commands.is_owner()
async def load(ctx, *, name: str):
	try:
		bot.load_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'"{name}" Cog loaded')

# Unload Cog

@bot.command()
@commands.is_owner()
async def unload(ctx, *, name: str):
	try:
		bot.unload_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'"{name}" Cog unloaded')

# Reload Cog

@bot.command()
@commands.is_owner()
async def reload(ctx, *, name: str):
	try:
		bot.reload_extension(f"cogs.{name}")
	except Exception as e:
		return await ctx.send(default.traceback_maker(e))
	await ctx.send(f'"{name}" Cog reloaded')

# Read Cogs

for file in os.listdir("./cogs"):
	if file.endswith(".py"):
		name = file[:-3]
		bot.load_extension(f"cogs.{name}")

# Run Bot

try:
	with open('./config.json') as f:
		token = json.load(f).get('token') or os.environ.get('token')
	bot.run(token, reconnect=True)
except Exception as e:
	print(e)
