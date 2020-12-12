import os
import json
import pymongo

from pymongo import MongoClient
from utils import default
from utils.data import Bot, HelpFormat

#DB

DB_UserName = 'RedSafe-Bot'

DB_Password = 'F0H5XARYJt69SD9l'

cluster = MongoClient(f'mongodb+srv://{DB_UserName}:{DB_Password}@redsafe.hoqeu.mongodb.net/RedSafe?retryWrites=true&w=majority')
db = cluster['RedSafe']
#DB
		
config = default.get("config.json")
print("Client Connecting")

def prefix(client, message):
	prefix_from_db = db['Prefixes']
	return prefix_from_db.find(message.guild.id)

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
