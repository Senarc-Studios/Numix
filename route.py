from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc

app = Quart(__name__)
ipc_client = ipc.Client(secret_key = "Swas")

app.config["SECRET_KEY"] = "test123"
app.config["DISCORD_CLIENT_ID"] = 744865990810271785   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "imKDsftXGNQ9WkGgbQ5U6i2XOFOzbg_B"   # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "https://dash.numix.xyz/callback"   

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
	return await render_template("index.html")

@app.route("/login")
async def login():
	return await discord.create_session()

@app.route("/callback")
async def callback():
	try:
		await discord.callback()
	except:
		return redirect(url_for("login"))

	user = await discord.fetch_user()
	return f"{user.name}#{user.discriminator}" #You should return redirect(url_for("dashboard")) here

@app.route("/dashboard")
async def dashboard():
	guild_count = await ipc_client.request("get_guild_count")
	guild_ids = await ipc_client.request("get_guild_ids")

	try:
		user_guilds = await discord.fetch_guilds()
	except:
		return redirect(url_for("login")) 

	same_guilds = []

	for guild in user_guilds:
		if guild.id in guild_ids:
			same_guilds.append(guild)


	return await render_template("dashboard.html", guild_count = guild_count, matching = same_guilds)

if __name__ == "__main__":
	app.run(debug=True)