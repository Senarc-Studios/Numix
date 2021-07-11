from numix_imports import *
import datetime
from datetime import datetime

config = default.get("./config.json")

def build_log_embed(action, member, mod, reason):
	if action == "ban":
		embed = discord.Embed(timestamp=datetime.now().timestamp(), colour=242424)
		embed.set_author(name=f"{member.name} {action.capitalize()}ned", icon_url=mod.avatar_url)
		embed.add_field(name="Moderator:", value=f"{mod.name}#{mod.discriminator}(`{mod.id}`)")
		embed.add_field(name="Member:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
		embed.add_field(name="Reason:", value=f"{reason}")
		embed.set_footer(text="Numix Premium", icon_url=config.logo)
	elif action == "kick":
		embed = discord.Embed(timestamp=datetime.now().timestamp(), colour=242424)
		embed.set_author(name=f"{member.name} {action.capitalize()}ed", icon_url=mod.avatar_url)
		embed.add_field(name="Moderator:", value=f"{mod.name}#{mod.discriminator}(`{mod.id}`)")
		embed.add_field(name="Member:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
		embed.add_field(name="Reason:", value=f"{reason}")
		embed.set_footer(text="Numix Premium", icon_url=config.logo)
	elif action == "channel_delete":
		embed = discord.Embed(timestamp=datetime.now().timestamp(), colour=242424)
		embed.set_author(name=f"{mod.name} deleted {member.name}", icon_url=mod.avatar_url)
		embed.add_field(name="Moderator:", value=f"{mod.name}#{mod.discriminator}(`{mod.id}`)")
		embed.add_field(name="Channel:", value=f"{member.name}(`{member.id}`)")
		embed.add_field(name="Reason:", value=f"{reason}")
		embed.set_footer(text="Numix Premium", icon_url=config.logo)
	return embed

async def log(action, guild, member, mod, reason):
	cluster = MongoClient(config.db1)
	collection = cluster.DataBase_1.settings
	for i in collection.find({ "_id": guild.id }):
		lcid = i["log"]
		log_channel = discord.get(guild.text_channels, id=lcid)
		embed = build_log_embed(action, member, mod, reason)
		await log_channel(embed=embed)