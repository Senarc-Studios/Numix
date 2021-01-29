import discord
from discord.ext import commands
import requests
from utils import default
from discord.utils import get


class rough(commands.Cog):
		def __init__(self, bot):
			self.bot = bot
			self.config = default.get("./config.json")
			print('"Rough" cog loaded')
		
		@commands.command()
		async def serverinfo(self, ctx):

			default_notification_setting = f"{ctx.guild.default_notifications}"
			default_notification_converter = default_notification_setting.replace("NotificationLevel.only_mentions", "Only @mentions")
			default_notification = default_notification_converter.replace("NotificationLevel.all_messages", "All Messages")
			owner = get(self.bot.users, id=ctx.guild.owner_id)

			date_1 = f"{ctx.guild.created_at.__format__('%d-%B-%Y @ %H:%M:%S')}"
			date_2 = date_1.replace("January", "1")
			date_3 = date_2.replace("February", "2")
			date_4 = date_3.replace("March", "3")
			date_5 = date_4.replace("April", "4")
			date_6 = date_5.replace("May", "5")
			date_7 = date_6.replace("June", "6")
			date_8 = date_7.replace("July", "7")
			date_9 = date_8.replace("August", "8")
			date_10 = date_9.replace("September", "9")
			date_11 = date_10.replace("October", "10")
			date_12 = date_11.replace("November", "11")
			date_13 = date_12.replace("December", "12")
			creation_date = date_13

			if ctx.guild.mfa_level == 0:

				guild = ctx.guild
				e = sum([1 for m in ctx.guild.members if m.bot])
				humans = sum(not member.bot for member in ctx.guild.members)
				embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
				embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
				embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
				embed.add_field(name="Server Region:", value=f"`{ctx.guild.region}`", inline=False)
				embed.add_field(name="Owner:", value=f"{owner.name}#{owner.discriminator}(`{owner.id}`)", inline=True)
				embed.add_field(name = "Server ID:", value=f"`{ctx.guild.id}`", inline=False)
				embed.add_field(name="Verification Level:", value=f"`{ctx.guild.verification_level}`", inline=True)
				embed.add_field(name="2FA requirement for mods:", value=f"`Disabled`", inline=False)
				embed.add_field(name="Default Notification Level:", value=f"`{default_notification}`", inline=True)
				embed.add_field(name="Boosts:", value=f"`{(ctx.guild.premium_subscription_count)}`", inline=False)
				embed.add_field(name="Boost Tier:", value=f"`{ctx.guild.premium_tier}`", inline=True)
				embed.add_field(name="Guild Creation Time:", value=f"`{creation_date}`", inline=False)
				embed.add_field(name="Total Members:", value=f"`{ctx.guild.member_count}`", inline=True)
				embed.add_field(name="Bots:", value=f"`{e}`", inline=False)
				embed.add_field(name="Humans:", value=f"`{humans}`", inline=True)
				embed.add_field(name="Roles:", value=f"`{len(ctx.guild.roles)}`", inline=False)
				embed.add_field(name="Voice Channels:", value=f"`{len(guild.voice_channels)}`", inline=True)
				embed.add_field(name="Text Channels:", value=f"`{len(guild.text_channels)}`", inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)

			elif ctx.guild.mfa_level == 1:
				
				guild = ctx.guild
				e = sum([1 for m in ctx.guild.members if m.bot])
				humans = sum(not member.bot for member in ctx.guild.members)
				embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
				embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon_url}")
				embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
				embed.add_field(name="Server Region:", value=f"`{ctx.guild.region}`", inline=False)
				embed.add_field(name="Owner:", value=f"{owner.name}#{owner.discriminator}(`{owner.id}`)", inline=True)
				embed.add_field(name = "Server ID:", value=f"`{ctx.guild.id}`", inline=False)
				embed.add_field(name="Verification Level:", value=f"**{ctx.guild.verification_level}**", inline=True)
				embed.add_field(name="Server 2FA:", value=f"Enabled", inline=False)
				embed.add_field(name="Default Notification Level:", value=f"{default_notification}", inline=True)
				embed.add_field(name="Boosts:", value=f"`{(ctx.guild.premium_subscription_count)}`", inline=False)
				embed.add_field(name="Boost Tier:", value=f"`{ctx.guild.premium_tier}`", inline=True)
				embed.add_field(name="Guild Creation Time:", value=f"`{creation_date}`", inline=False)
				embed.add_field(name="Total Members:", value=f"`{ctx.guild.member_count}`", inline=True)
				embed.add_field(name="Bots:", value=f"`{e}`", inline=False)
				embed.add_field(name="Humans:", value=f"`{humans}`", inline=True)
				embed.add_field(name="Roles:", value=f"`{len(ctx.guild.roles)}`", inline=False)
				embed.add_field(name="Voice Channels:", value=f"`{len(guild.voice_channels)}`", inline=True)
				embed.add_field(name="Text Channels:", value=f"`{len(guild.text_channels)}`", inline=False)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)
		
		@commands.command(aliases=["av"])
		async def avatar(self, ctx, member: discord.User = None):
				if member is None:
					member = ctx.message.author
				else:
					pass
				a = member.avatar_url
				embed = discord.Embed(timestamp=ctx.message.created_at, color=0x3df08a)
				embed.set_author(name=f"{member.name}#{member.discriminator}'s avatar", icon_url=f"{a}")
				embed.set_image(url=f"{a}")
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)

def setup(bot):
		bot.add_cog(rough(bot))