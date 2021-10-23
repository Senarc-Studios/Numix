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
from numix_imports import *
import datetime
from datetime import datetime

config = default.get("./config.json")

def build_log_embed(action, member, mod, reason):
	if action == "ban":
		embed = discord.Embed(timestamp=datetime.now().timestamp(), colour=242424)
		embed.set_author(name=f"{member.name} {action.capitalize()}ned", icon_url=mod.display_avatar)
		embed.add_field(name="Moderator:", value=f"{mod.name}#{mod.discriminator}(`{mod.id}`)")
		embed.add_field(name="Member:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
		embed.add_field(name="Reason:", value=f"{reason}")
		embed.set_footer(text="Numix Premium", icon_url=config.logo)
	elif action == "kick":
		embed = discord.Embed(timestamp=datetime.now().timestamp(), colour=242424)
		embed.set_author(name=f"{member.name} {action.capitalize()}ed", icon_url=mod.display_avatar)
		embed.add_field(name="Moderator:", value=f"{mod.name}#{mod.discriminator}(`{mod.id}`)")
		embed.add_field(name="Member:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
		embed.add_field(name="Reason:", value=f"{reason}")
		embed.set_footer(text="Numix Premium", icon_url=config.logo)
	elif action == "channel_delete":
		embed = discord.Embed(timestamp=datetime.now().timestamp(), colour=242424)
		embed.set_author(name=f"{mod.name} deleted {member.name}", icon_url=mod.display_avatar)
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