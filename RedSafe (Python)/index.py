import os
import json
import pymongo

from pymongo import MongoClient
from utils import default
from utils.data import Bot, HelpFormat

#DB
cluster = MongoClient('mongodb+srv://RedSafe-Bot:F0H5XARYJt69SD9l@redsafe.hoqeu.mongodb.net/RedSafe?retryWrites=true&w=majority')
db = cluster['RedSafe']
#DB
# i flipppin like muffins		
config = default.get("config.json")
print("Client Connecting")

def prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]

bot = Bot(
	command_prefix=prefix,
	prefix=prefix,
	command_attrs=dict(hidden=True)
)

bot.remove_command('help')

for file in os.listdir("./cogs"):
	if file.endswith(".py"):
		name = file[:-3]
		bot.load_extension(f"cogs.{name}")

try:
	bot.run(config.token)
except Exception as e:
	print(f'Error when logging in: {e}')
