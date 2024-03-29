import os
import sys
import ctypes
import asyncio

from cool_utils import JSON
from motor.motor_asyncio import AsyncIOMotorClient

windows = sys.platform == 'win32'

try:
	import click
except:
	if windows:
		os.system("pip install click")
	else:
		os.system("python3 -m pip install click")

def _await(function):
	return asyncio.run(function)

def admin_access():
	try:
		is_admin = (os.getuid() == 0)
	except AttributeError:
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
	
	return is_admin

@click.command(
	name = 'setup',
	help = "Setup command to prepare the bot for runtime."
)
@click.option(
	"-d",
	"--debug",
	is_flag = True,
	default = False,
	help = "Enables debug mode"
)
@click.option(
	"-r",
	"--reset-db",
	is_flag = True,
	default = False,
	help = "Resets the database"
)
@click.argument(
	"-t",
	"--token",
	help = "Sets the bot token"
)
@click.argument(
	"-m",
	"--mongo-url",
	help = "Stores the mongo url"
)
@click.argument(
	"-o",
	"--owner",
	help = "Stores the owner id"
)
@click.argmuent(
	"-cg",
	"--core-guild",
	help = "Stores the Core Guild (Discord Server) id"
)
@click.pass_context
def setup(ctx, debug: bool, reset_db: bool, token: str, mongo_url: str, owner: str, core_guild: str):
	if reset_db:
		for database in _await(AsyncIOMotorClient(mongo_url).list_databases()):
			click.echo(f"[DEBUG]: Deleting `{database}` database...") if debug else None
			_await(AsyncIOMotorClient(mongo_url).drop_database(database))
		click.echo("All databases deleted.")

	JSON.open("../mongo.json")
	JSON.write("MONGO", mongo_url)

	try:
		int(owner)
	except:
		click.echo("Invalid owner id.")
		click.echo("[DEBUG]: Aborting setup due to invalid owner id.") if debug else None
		return

	try:
		int(core_guild)
	except:
		click.echo("Invalid core guild id.")
		click.echo("[DEBUG]: Aborting setup due to invalid core guild id.") if debug else None
		return

	_await(
		AsyncIOMotorClient(mongo_url)["numix"]["config"].insert_one(
			{
				"_id": "setup",
				"owner": int(owner),
				"core_guild": int(core_guild),
				"token": token
			}
		) if token is not None else AsyncIOMotorClient(mongo_url)["numix"]["config"].insert_one(
			{
				"_id": "setup",
				"owner": int(owner),
				"core_guild": int(core_guild),
			}
		)
	)

	if windows:
		click.echo("[DEBUG]: Running windows pip for dependency install...") if debug else None
		os.system("pythonw -m pip install -U -r ./requirements.txt")
		click.echo("[DEBUG]: Sleeping for 10 seconds to ensure full dependency install...") if debug else None
		asyncio.run(asyncio.sleep(10))

	else:
		click.echo("[DEBUG]: Running standard pip for dependency install")
		os.system("nohup python3 -m pip install -U -r ./requirements.txt &")
		click.echo("[DEBUG]: Sleeping for 10 seconds to ensure full dependency install...") if debug else None
		asyncio.run(asyncio.sleep(10))

	click.echo("Installed all required Dependencies.")
	click.echo("Setup is complete, Exiting...")

@click.command(
	name = "run",
	help = "Runs the Discord Bot."
)
@click.option(
	"-bg",
	"--background",
	is_flag = True,
	help = "Make the bot run on the background instead of terminal."
)
@click.pass_context
def run(ctx, background: bool):
	if windows:
		os.system("pythonw ./main.py") if background else os.system("python ./main.py")

	else:
		os.system("nohup python3 ./main.py &") if background else os.system("python3 ./main.py")

@click.command(
	name = "update",
	help = "Updates from mainstream the bot."
)
@click.option(
	"-d",
	"--debug",
)
@click.option(
	"-r",
	"--reset",
	help = "Re-installs the bot from github latest build."
)
@click.pass_context
def update(ctx, debug: bool, reset: bool):
	if reset:
		if windows and admin_access():
			click.echo("[DEBUG]: Cloning Numix into temp folder from github...") if debug else None
			os.system("git clone https://github.com/Senarc-Studios/Numix.git ../temp")
			click.echo("[DEBUG]: Deleting Numix...") if debug else None
			os.system("rmdir /f /s ../Numix")
			click.echo("[DEBUG]: Moving Numix from temp folder to Numix...") if debug else None
			os.system("move ../temp/Numix ../Numix")

			click.echo("[DEBUG]: Installing dependencies...") if debug else None
			os.system("pythonw -m pip install -U -r ./requirements.txt")
			click.echo("[DEBUG]: Sleeping for 10 seconds to ensure full dependency install...") if debug else None
			asyncio.run(asyncio.sleep(10))
			click.echo("Re-installed Numix from latest build.")
			
			JSON.open("../mongo.json")
			mongo_url = JSON.get("MONGO")

			if mongo_url is not None:
				for database in _await(AsyncIOMotorClient(mongo_url).list_databases()):
					click.echo(f"[DEBUG]: Deleting `{database}` database...") if debug else None
				_await(AsyncIOMotorClient(mongo_url).drop_database(database))
				click.echo("All databases deleted.")
			return