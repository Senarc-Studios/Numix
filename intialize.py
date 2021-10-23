import os
os.system("pip install -U cool-utils")
os.system("python3 -m pip install -U cool-utils")

import utils

os.system(utils.get_command("pip") + " install -r requirements.txt")

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

	MongoClient(utils.get_data(file="config", variable="db1"))

main()