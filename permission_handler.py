from numix_imports import *

config = default.get("./config.json")

def permission(permission):

	async def predicate(ctx):
		if ctx.author.id in config.owners:
			return True

		elif permission == "administrator":
			if ctx.author.guild_permissions.administrator:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "manage_messages":
			if ctx.author.guild_permissions.manage_messages:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "kick":
			if ctx.author.guild_permissions.kick:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "ban":
			if ctx.author.guild_permissions.ban:
				return True
				
			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)

		elif permission == "manage_guild":
			if ctx.author.guild_permissions.manage_guild:
				return True

			else:
				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You do not meet the required guild permissions the command \"`{ctx.command.name}`\" requires to be executed.\n\nYou need `{permission.upper()}` Permission in this Guild to be able to execute/run/use this command.", color=242424)
				embed.set_author(name="Insufficient Permissions", icon_url=config.forbidden_img)
				embed.set_footer(text="Numix", icon_url=config.logo)
				await ctx.send(embed=embed)
		

	return commands.check(predicate)