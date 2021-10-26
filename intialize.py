import os
import sys
os.system("pip install -U cool-utils")
os.system("python3 -m pip install -U cool-utils")

import utils

def get_command(command: str):
	PYTHON = {
		'linux': 'python3',
		'win32': 'python',
		'macos': 'python3'
	}

	PIP = {
		'linux': 'python3 -m pip',
		'win32': 'pip',
		'macos': 'python3 -m pip'
	}

	CLEAR = {
		'linux': 'clear',
		'win32': 'cls',
		'macos': 'clear'
	}

	LS = {
		'linux': 'ls',
		'win32': 'dir',
		'macos': 'ls'
	}
	command = command.lower()
	if command == "python":
		return PYTHON[sys.platform]

	elif command == "pip":
		return PIP[sys.platform]

	elif command == "clear":
		return CLEAR[sys.platform]

	elif command == "ls":
		return LS[sys.platform]

	else:
		return command

os.system(get_command("pip") + " install -r requirements.txt")

def main():
	try:
		token = input("Paste your bot's Token: ")
		utils.register_value(file="config", variable="token", value=token)
		logo = input("Paste your bot's avatar link: ")
		utils.register_value(file="config", variable="logo", value=logo)
		lab = int(input("Paste your bot lab's Server ID: "))
		utils.register_value(file="config", variable="supportserver", value=lab)
		error = (input("Paste your Error log webhook url: "))
		utils.register_value(file="config", variable="error_webhook", value=error)
		interaction = int(input("Paste your interaction log channel ID: "))
		utils.register_value(file="config", variable="interaction_log", value=interaction)
		debug = int(input("Paste your debug channel ID: "))
		utils.register_value(file="config", variable="debug_channel", value=debug)
		mongo = input("Paste your MongoURL: ")
		utils.register_value(file="config", variable="db1", value=mongo)
		success = input("Paste your Success Emoji: ")
		utils.register_value(file="config", variable="success", value=success)
		forbidden = input("Paste your Fail Emoji: ")
		utils.register_value(file="config", variable="forbidden", value=forbidden)
		arrow = input("Paste the emoji used as a arrow: ")
		utils.register_value(file="config", variable="arrow", value=arrow)
		user = input("What is your Discord username and tag? ")
		utils.register_value(file="config", variable="devs", value=f"`{user}`")
		id = int(input("What is your Discord ID? "))
		utils.register_value(file="config", variable="owners", value=[id])
		utils.register_value(file="config", variable="break_bank_limit", value=[id])
	except:
		raise TypeError(f"An unsupported input recieved while initializing bot.")



def reset_database():
	import pymongo
	from pymongo import MongoClient

	new_databases = ["Moderation", "DataBase_1", "Economy"]
	moderation_collections = ["warns"]
	db1_collections = ["Leveling", "assets", "filter", "interactions", "nucrypt", "nukeban", "nukekick", "prefixes", "profiles", "settings", "assets", "interactions"]
	economy_collections = ["bank", "credentials", "money", "transaction_logs"]

	mongo_client =  MongoClient(utils.get_data(file="config", variable="db1"))
	db_list = mongo_client.database_names()
	for database in db_list:
		mongo_client.drop_database(database)

	for db in new_databases:
		print(mongo_client[db])

	for collection in db1_collections:
		db = mongo_client["DataBase_1"]
		print(db[collection])

	for collection in economy_collections:
		db = mongo_client["Economy"]
		print(db[collection])

	for collection in moderation_collections:
		db = mongo_client["Moderation"]
		print(db[collection])

	db = mongo_client["DataBase_1"]	
	db["assets"].insert_one({"_id": "badges", "premium_users": [], "partnered_users": [], "verified_users": [], "beta_testers": []})
	db["assets"].insert_one({"_id": "debug", "value": True})
	db["interactions"].insert_one({"_id": "all", "uses": 0})
	print("\n\nDatabase and bot fully initialized.")

main()
reset_database()