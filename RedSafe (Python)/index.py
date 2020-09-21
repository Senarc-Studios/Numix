import discord
import asyncio
from discord.ext import commands
import time
import json




redsafelogo = 'https://cdn.discordapp.com/attachments/731716869576327201/743393021936140358/RedSafe_Logo1.png'
client = discord.Client()
TOKEN = "NTQ1MjMwMTM2NjY5MjQxMzY1.XGQXIg.FSmA_URgc0pT71aGfLPtOaoaSXM"
client = commands.Bot(command_prefix = '.')
client.remove_command('help')

prefixes = ['.','!','s.','k!']
ser_pref={'server id':['.',',']}
def get_prefix(bot, msg):
    if msg.server.id in ser_pref:
        return commands.when_mentioned_or(*ser_pref['server id'])


    return commands.when_mentioned_or(*prefixes)(bot, msg)

client = commands.Bot(command_prefix=get_prefix)

status4 = 'You type ".help"'
status1 = 'You type ".help"'
status2 = 'Discord API'
status3 = 'RedSafe Premium'
status1 = f"{len(client.guilds)} Servers"

async def status_task():
    while True:
        global count
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status1))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status2))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status3))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status4))
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{count} Servers"))
        await asyncio.sleep(10)



@client.event
async def on_ready():
    client.loop.create_task(status_task())
    global count
    print('Bot ready')

    count = 0
    for guild in client.guilds:
        print("Connected to server: {}".format(guild))
        count +=1

    client.loop.create_task(status_task())



@client.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="> Command Categories", description='`.config` - Config Commands \n `moderation` - Moderation Commands \n `general` - General commands anyone can use. \n `staff` - Commands that will help the staff members. \n `music` - Music Commands! \n `premium` - **Premium** Commands that will only work if you get **premium**. \n \n *You can do ".help <category>" to view the commands.*', color=0xadd8e6)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@help.command(name="config")
async def help_config(ctx):
    embed = discord.Embed(title='> Config Commands', description='`.set-welcome` - Sets the welcome channel and notifies when someone joins. \n \n `.set-mute` - Sets the mute role which is used in .mute \n \n `.set-report` - Sets the report log channel, Usage - **.set-report <#channel>** \n \n `.set-suggestion` - Sets the suggestion channel. \n \n `.links off` - Turns **off** all links and denies links to be sent. \n \n `.links on` - Turns **on** and allows links to be sent. \n \n `.verification <on/off/set>` - **Set/On/Off** a verification system.', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="moderation")
async def help_moderation(ctx):
    embed = discord.Embed(title='> Moderation Commands', description='', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="general")
async def help_general(ctx):
    embed = discord.Embed(title='> General Commands', descrition='', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="staff")
async def help_staff(ctx):
    embed = discord.Embed(title='> Staff Commands', description='', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="music")
async def help_music(ctx):
    embed = discord.Embed(title='> Music Commands', description='', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="premium")
async def help_premium(ctx):
    embed = discord.Embed(title='> Premium Commands', description='', color=0xff0000)
    embed.set_footer(text='RedSafe Premium', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    before_ws = int(round(client.latency * 1000, 1))
    message = await ctx.send("🏓 Pong")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f":zap: WS: {before_ws}ms  | :star:  REST: {int(ping)}ms")

@client.command()
async def userinfo(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.message.author
    if user.activity is not None:
        game = user.activity.name
    else:
        game = None
    voice_state = None if not user.voice else user.voice.channel
    embed = discord.Embed(timestamp=ctx.message.created_at)
    embed.add_field(name='User ID', value=user.id, inline=True)
    embed.add_field(name='Nick', value=user.nick, inline=True)
    embed.add_field(name='Status', value=user.status, inline=True)
    embed.add_field(name='On Mobile', value=user.is_on_mobile(), inline=True)
    embed.add_field(name='In Voice', value=voice_state, inline=True)
    embed.add_field(name='Game', value=game, inline=True)
    embed.add_field(name='Highest Role', value=user.top_role.name, inline=True)
    embed.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    embed.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)
    emoji_count = len(ctx.guild.emojis)
    channel_count = len([x for x in ctx.guild.channels if isinstance(x, discord.channel.TextChannel)])
    embed = discord.Embed(timestamp=ctx.message.created_at)
    embed.add_field(name='Name (ID)', value=f"{ctx.guild.name} ({ctx.guild.id})")
    embed.add_field(name='Owner', value=ctx.guild.owner, inline=False)
    embed.add_field(name='Members', value=ctx.guild.member_count)
    embed.add_field(name='Text Channels', value=str(channel_count))
    embed.add_field(name='Region', value=ctx.guild.region)
    embed.add_field(name='Verification Level', value=str(ctx.guild.verification_level))
    embed.add_field(name='Highest role', value=ctx.guild.roles[-1])
    embed.add_field(name='Number of roles', value=str(role_count))
    embed.add_field(name='Number of emotes', value=str(emoji_count))
    embed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, reason=None):
    role = discord.utils.get(ctx.guild.roles, name=MODERATION_ROLE)
    logs = client.get_channel(LOGGING_CHANNEL)
    if role in ctx.author.roles:
        """Bans a user"""
        if reason == None:
            await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
        else:
            memberstr = str(member)
            await logs.send(ctx.message.author.mention + " has banned person " + memberstr)
            ban = discord.Embed(title="New Ban", color=0x37cdaf)
            ban.add_field(name="Moderator", value=ctx.message.author.mention, inline=True)
            ban.add_field(name="Banned", value=f"{member.name}#{member.discriminator} <@" + str(member.id) + ">" + f"({member.id})", inline=True)
            await logs.send(embed=ban)
            await ctx.send(f"{member.name}#{member.discriminator}" + " has been banned for " + reason)
            messageok = f"You have been banned from {ctx.guild.name} for {reason}"
            await member.send(messageok)
            await member.ban(reason=f"Moderator:{ctx.message.author.name} Reason:" + reason)
    else:
        await ctx.send("You do not have permission to run this command, silly!")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, reason=None):
    role = discord.utils.get(ctx.guild.roles, name=MODERATION_ROLE)
    logs = client.get_channel(LOGGING_CHANNEL)
    if role in ctx.author.roles:
        """Kicks a user"""
        if reason == None:
            await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
            embed = discord.Embed(title="Attempt at Kick", color=0x37cdaf)
            embed.add_field(name="Command Issuer", value=ctx.message.author.mention, inline=True)
            embed.add_field(name="Attempted to kick but forgot reason", value=f"{member.name}#{member.discriminator} <@" + str(member.id) + ">" + f"({member.id})", inline=True)
        else:
            memberstr = str(member)
            await logs.send(ctx.message.author.mention + " has kicked person " + memberstr)
            kick = discord.Embed(title="Kick", color=0x37cdaf)
            kick.add_field(name="Moderator", value=ctx.message.author.mention, inline=True)
            kick.add_field(name="Kicked", value=f"{member.name}#{member.discriminator} <@" + str(member.id) + ">" + f"({member.id})", inline=True)
            await ctx.send(embed=kick)
            message = f"You have been kicked from {ctx.guild.name} for {reason}"
            await member.send(message)
            await member.kick(reason=f"Moderator:{ctx.message.author.name} Reason:" + reason)

@kick.error
async def kick_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that!")

client.run(TOKEN)
