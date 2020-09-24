import discord
import asyncio
from discord.ext import commands
import time
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from utils import permissions, default
from discord.utils import get
from discord.ext import commands,tasks
from discord.ext.commands import errors
import re


redsafelogo = 'https://cdn.discordapp.com/attachments/731716869576327201/743393021936140358/RedSafe_Logo1.png'
client = discord.Client()
TOKEN = "NTQ1MjMwMTM2NjY5MjQxMzY1.XGQXIg.FSmA_URgc0pT71aGfLPtOaoaSXM"

def prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = prefix)

client.remove_command('help')

status4 = 'You type ".help"'
status2 = 'Discord API'
status3 = 'RedSafe Premium'

async def status_task():
    while True:
        global count
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status4))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status2))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status3))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{count} Servers"))
        await asyncio.sleep(10)



@client.event
async def on_ready():
    client.loop.create_task(status_task())
    global count
    print('Bot ready')
    print("RedSafe Active!")
    count = 0
    for guild in client.guilds:
        print("Connected to server: {}".format(guild))
        count +=1

    client.loop.create_task(status_task())

@client.event
async def on_message(ctx):
    if ctx.content.find(f"<@!{client.user.id}>") != -1:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        embed = discord.Embed(title='> Prefix', description=f"""The current prefix for this server is set to `{prefixes[str(ctx.guild.id)]}`""", color=0x00ff00)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
        await ctx.channel.send(embed=embed)


#@client.event
#async def on_message(ctx):
#    if ctx.content.find(f".com", '.net', '.tk', '.uk', 'www.', 'http') != -1:
#        member = discord.Member if not discord.Member else discord.Member
#        embed = discord.Embed(title=f'{message.guild.name}', description=f'You are not allowed to send links on **{message.guild.name}**.')
#        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
#        ctx.member.send(embed=embed)
#        await ctx.message.delete()

    await client.process_commands(ctx)

with open('badwords.txt','r') as f:
    bad_words = '|'.join(s for l in f for s in l.split(', '))
    bad_word_checker = re.compile(bad_words).search

@client.event
async def on_message(message):
    if not message.author.bot:
        with open('swearfilterboi.json', 'r') as f:
            prefixes = json.load(f)
        if prefixes[str(message.guild.id)] == "enabled":
            if bad_word_checker(message.content):
                await message.delete()
                embed = discord.Embed(text=f'{ctx.guild.name}', description=f"Hey! You aren't allowed swear on {ctx.guild.name}")
                embed.set_footer(text='RedSafe Premium', icon_url=redsafelogo)
                member.send(embed=embed)
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    with open('onjoinconfigset.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(member.guild.id)]
    with open('onjoinconfig.json', 'r') as f:
        joe = json.load(f)
    joes = joe[str(member.guild.id)]
    print(joes)
    if joes == "enabled":
        channel = client.get_channel(prefix)
        embed = discord.Embed(title=f'{member.name} Joined', description=f'Hey {member.name}, Welcome to **{member.guild.name}** \n Have a nice stay!', color=242424)
        embed.set_image(url='https://cdn.discordapp.com/attachments/731716869576327201/744818377461071952/Welcome-Black-Text-White-BG.gif')
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    with open('onleaveconfigset.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(member.guild.id)]
    with open('onleaveconfig.json', 'r') as f:
        joe = json.load(f)
    joes = joe[str(member.guild.id)]
    print(joes)
    if joes == "enabled":
        channel = client.get_channel(prefix)
        embed = discord.Embed(title=f'{member.name} Left', description=f'{member.name} Left **{member.guild.name}** Bye! \n Hope you join back.', color=0xff0000)
        embed.set_image(url='https://media.giphy.com/media/3o6ZtcOxQ9vi8vb9Cg/giphy.gif')
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

@client.group()
@commands.has_permissions(administrator=True)
async def swear(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='Swear Filter', description=f'You can turn **on**, or **off** the Swear Filter if you have RedSafe Premium. \n Usage: \n \n `{prefix}swear on` - Turns on the Swear Filter. \n `{prefix}swear off` - Turns off the Swear Filter.', color=0x00ff00)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@swear.command(name="on")
@commands.has_permissions(administrator=True)
async def swear_on(ctx):

 async def premium_check(ctx):
         with open('rspremium.json', 'r') as f:
             rscheck = json.load(f)

         premium = rscheck[str(ctx.guild.id)]
              if premium == "enabled":

                with open('swearfilterboi.json', 'r') as f:
                   verify = json.load(f)

                 verify[str(ctx.guild.id)] = "enabled"

    with open('swearfilterboi.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Swear Filter', description=f'The Swear Filter has been **Enabled**', color=0x00ff00)
    embed.set_footer(text='RedSafe Premium', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@swear.command(name="off")
@commands.has_permissions(administrator=True)
async def swear_off(ctx):

    with open('swearfilterboi.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('swearfilterboi.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Swear Filter', description=f'The Swear Filter has been **Disabled**', color=0x00ff00)
    embed.set_footer(text='RedSafe Premium', icon_url=redsafelogo)
    await ctx.send(embed=embed)






@client.group()
@commands.has_permissions(administrator=True)
async def welcome(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='RedSafe Welcome', description=f'You can turn **on**, **off**, or **set** Welcome message. \n Usage: \n \n `{prefix}welcome on` - Turns on the Welcome Messages. \n `{prefix}welcome off` - Turns off the Welcome Messages. \n `{prefix}welcome set <#channel>` - Set the welcome channel.', color=0x00ff00)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@welcome.command(name="on")
@commands.has_permissions(administrator=True)
async def welcome_on(ctx):

    with open('onjoinconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "enabled"

    with open('onleaveconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='RedSafe Welcome', description=f'Welcome Message has been **Enabled**', color=0x00ff00)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@welcome.command(name="off")
@commands.has_permissions(administrator=True)
async def welcome_off(ctx):

    with open('onjoinconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('onjoinconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='RedSafe Welcome', description=f'Welcome Message has been **Disabled**', color=0xff0000)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@welcome.command(name="set")
@commands.has_permissions(administrator=True)
async def welcome_set(ctx, string):

    with open('onjoinconfigset.json', 'r') as f:
        verify = json.load(f)

    boop = int(re.search(r'\d+', string).group(0))

    verify[str(ctx.guild.id)] = boop

    with open('onjoinconfigset.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='RedSafe Welcome', description=f'The Welcome Channel been set to {string}', color=0x00ff00)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.group()
@commands.has_permissions(administrator=True)
async def leave(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='RedSafe leave', description=f'You can turn **on**, **off**, or **set** leave message. \n Usage: \n \n `{prefix}leave on` - Turns on the leave Messages. \n `{prefix}leave off` - Turns off the leave Messages. \n `{prefix}leave set <#channel>` - Set the leave channel.', color=0x00ff00)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@leave.command(name="on")
@commands.has_permissions(administrator=True)
async def leave_on(ctx):

    with open('onleaveconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "enabled"

    with open('onleaveconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Leave Message', description=f'The Leave Message has been **Enabled**', color=0x00ff00)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@leave.command(name="off")
@commands.has_permissions(administrator=True)
async def leave_off(ctx):

    with open('onleaveconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('onleaveconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Leave Message', description=f'The Leave Message has been **Disabled**', color=0xff0000)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@leave.command(name="set")
@commands.has_permissions(administrator=True)
async def leave_set(ctx, string):

    with open('onleaveconfigset.json', 'r') as f:
        verify = json.load(f)

    boop = int(re.search(r'\d+', string).group(0))

    verify[str(ctx.guild.id)] = boop

    with open('onleaveconfigset.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Leave Message', description=f'The Leave Message Channel been set to {string}', color=0x00ff00)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)









@client.event
async def on_guild_remove(guild):
    global count
    count -=1
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758248651515625503/r4JCjSTWZ9ly3sxnYjzjzF3g1saIgEqGY_cXxg6hmexnnhcokk_IM1qm138li0Judg2p')
    embed = DiscordEmbed(title='Left Guild!', description=f"Guild : {guild.name} \n \n ID : {guild.id} \n \n Owner : {guild.owner}", color=242424)
    webhook.add_embed(embed)
    webhook.execute()

@client.group()
async def prefix(ctx):
    if ctx.invoked_subcommand is None:
       with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

       embed = discord.Embed(title='> Prefix', description=f"""The current prefix for this server is set to `{prefixes[str(ctx.guild.id)]}`""", color=0x00ff00)
       embed.set_footer(text='RedSafe', icon_url=redsafelogo)
       await ctx.send(embed=embed)

@prefix.command(name="set")
@commands.has_permissions(administrator=True)
async def prefix_set(ctx, prefix):

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    embed = discord.Embed(title='Prefix', description=f'The bot prefix has been set to `{prefix}`', color=0x00ff00)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.event
async def on_guild_join(guild):
    global count
    count +=1
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758248651515625503/r4JCjSTWZ9ly3sxnYjzjzF3g1saIgEqGY_cXxg6hmexnnhcokk_IM1qm138li0Judg2p')
    embed = DiscordEmbed(title='New Guild Join!', description=f"Guild : {guild.name} \n \n ID : {guild.id} \n \n Owner : {guild.owner}", color=242424)
    webhook.add_embed(embed)
    webhook.execute()
    embed = discord.Embed(title='RedSafe', description='Hello There, This is RebootSafe. \n My prefix default is `.` You can change it with `.prefix set {prefix}` \n Have a nice day!', color=0xFFA500)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    try:
        to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
    except IndexError:
        pass
    else:
        link = await to_send.create_invite(max_age=0)
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758248651515625503/r4JCjSTWZ9ly3sxnYjzjzF3g1saIgEqGY_cXxg6hmexnnhcokk_IM1qm138li0Judg2p')
        embed = DiscordEmbed(title='New Guild Join!', description=f"Guild : {guild.name} \n \n ID : {guild.id} \n \n Owner : {guild.owner} \n \n Invite : {link}", color=242424)
        webhook.add_embed(embed)
        webhook.execute()
        await to_send.send(embed=embed)


@client.command()
async def megahonk(ctx):
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/757575792271294596/JzkFCovOEduKc3zPNlPw_Wvqxb5aPT1eJmwQcB4-Kay7OwetSuoLkuahlLenZm1Y4bMI')
    embed = DiscordEmbed(title='Your Title', description=f"<@!259875936852246528> MEGA HONK FROM {ctx.author.name} {ctx.author.id}", color=242424)
    webhook.add_embed(embed)
    webhook.execute()
    await ctx.send("I have sent a Mega Honk :)")

@client.command()
@commands.cooldown(1, 300, commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def dm(ctx, user_id: int, *, message: str):
    """ DM the user of your choice """
    user = client.get_user(user_id)
    if not user:
        return await ctx.send(f"Could not find any UserID matching **{user_id}**")

    try:
        embed = discord.Embed(title=f"{ctx.guild.name}", description=f"New message from **{ctx.guild.name}**'s Staff \n \n  Message - {message}", color=0x1868af)
        await user.send(embed=embed)
        await ctx.send(f"✉️ Sent a DM to **{user_id}**")
    except discord.Forbidden:
        await ctx.send("This user might be having DMs blocked or it's a bot account...")

@client.event
async def on_command_error(ctx, err):
    if isinstance(err, errors.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.2f} seconds.")
    else:
        print(err)


@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason: str = None):
    """ Mutes a user from the current server. """
    if await permissions.check_priv(ctx, member):
        return

    muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

    if not muted_role:
        return await ctx.send("Are you sure you've made a role called **Muted**? Remember that it's case sensetive too...")

    try:
        await member.add_roles(muted_role, reason=default.responsible(ctx.author, reason))
        await ctx.send(default.actionmessage("muted"))
        audit_logging = discord.utils.get(ctx.guild.channels, name="redsafe-logs")
        embed = discord.Embed(title=":mute: User muted: " + str(member.name) + " (" + str(member.id) + ") \n \n Responsible moderator: " + str(ctx.author) + " \n Reason: " + str(reason))
        await audit_logging.send(embed=embed)
        embed2 = discord.Embed(title=f'{ctx.guild.name}', description=f'You were muted in **{ctx.guild.name}** for : ```{str(reason)}```', color=0xff0000)
        embed2.set_footer(text='RedSafe', icon_url=redsafelogo)
        await member.send(embed=embed2)
    except Exception as e:
        if "object has no attribute" in str(e):
            await ctx.send("Please make sure to setup a Channel named #redsafe-logs so that I can log mutes / bans. " + ctx.message.author.mention)
        else:
            await ctx.send(e)

@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member, *, reason: str = None):
    """ Unmutes a user from the current server. """
    if await permissions.check_priv(ctx, member):
        return

    muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

    if not muted_role:
        return await ctx.send("Are you sure you've made a role called **Muted**? Remember that it's case sensetive too...")

    try:
        await member.remove_roles(muted_role, reason=default.responsible(ctx.author, reason))
        await ctx.send(default.actionmessage("unmuted"))
        audit_logging = discord.utils.get(ctx.guild.channels, name="redsafe-logs")
        embed = discord.Embed(title=":loud_sound: User unmuted: " + str(member.name) + " (" + str(member.id) + ") \n \n Responsible moderator: " + str(ctx.author) + " \n Reason: " + str(reason))
        await audit_logging.send(embed=embed)
        embed2 = discord.Embed(title=f'{ctx.guild.name}', description=f'You were unmuted in **{ctx.guild.name}**', color=0x00ff00)
        embed2.set_footer(text='RedSafe', icon_url=redsafelogo)
        await member.send(embed=embed2)
    except Exception as e:
        if "object has no attribute" in str(e):
            await ctx.send("Please make sure to setup a Channel named #redsafe-logs so that I can log unmutes / unbans. " + ctx.message.author.mention)
        else:
            await ctx.send(e)

@client.command()
@commands.has_permissions(administrator=True)
async def setlog(ctx, channel):
    print(channel)
    with open('rslogsetting.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = channel

    with open('rslogsetting.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Log', description=f'The Logs channel role been set to {channel}', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.group()
async def premium(ctx):
    if ctx.invoked_subcommand is None:
        print("boop")

@premium.command(name="check")
async def premium_check(ctx):
        with open('rspremium.json', 'r') as f:
            rscheck = json.load(f)

        premium = rscheck[str(ctx.guild.id)]
        embed = discord.Embed(title='RedSafe Premium', description=f'RedSafe Premium is currently {premium}', color=0x00ff00)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@client.group()
@commands.has_permissions(administrator=True)
async def verification(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='Verification', description=f'You can turn **on**, **off**, or **set** verified roles \n Usage: \n \n `{prefix}verification on` - Turns the verification system on. \n `{prefix}verification off` - Turns off the verification system. \n `{prefix}verification set <@role>` - sets a role that is given after verification.', color=0x00ff00)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@verification.command(name="on")
@commands.has_permissions(administrator=True)
async def verification_on(ctx):

    with open('verifysetting.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "enabled"

    with open('verifysetting.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Verification', description=f'The Verification System has been **Enabled**', color=0x00ff00)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@verification.command(name="off")
@commands.has_permissions(administrator=True)
async def verification_on(ctx):

    with open('verifysetting.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('verifysetting.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Verification', description=f'The Verification System has been **Disabled**', color=0x00ff00)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@verification.command(name="set")
@commands.has_permissions(administrator=True)
async def verification_set(ctx, role: discord.Role):

    with open('verify.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = role.id

    with open('verify.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Verification', description=f'The Verification System role been set to `{role}`', color=0x00ff00)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)



@client.command()
async def verify(ctx):
    with open('verifysetting.json', 'r') as f:
        verifysett = json.load(f)
    settingverify = verifysett[str(ctx.guild.id)]


    with open('verify.json', 'r') as f:
        verifi = json.load(f)
    verifyrole = verifi[str(ctx.guild.id)]

    if "enabled" == settingverify:
        for role in ctx.author.roles:
            if role.name == verifyrole:
                print("BOI ALREADY VERIFIED")
            print(role.name)
        role = get(ctx.guild.roles, id=verifyrole)
        await ctx.author.add_roles(role, reason="Verification System. User Verified")
        embed = discord.Embed(title='Verified', description=f'You have been verified on **{ctx.guild.name}**', color=0xFFA500)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)

        user = client.get_user(ctx.author.id)
        await user.send(embed=embed)

    else:
        await ctx.send("The Verification System has not been enabled.")

@client.command()
async def avatar(ctx, *, user: discord.Member = None):
    """ Get the avatar of you or someone else """
    user = user or ctx.author
    embed = discord.Embed(title=f"{user.name}'s avatar", color=0x00ff00)
    embed.set_image(url=user.avatar_url_as(size=1024))
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title="> Command Categories", description=f'`config` - Config Commands \n `moderation` - Moderation Commands \n `general` - General commands anyone can use. \n `staff` - Commands that will help the staff members. \n `music` - Music Commands! \n `premium` - **Premium** Commands that will only work if you get **premium**. \n \n *You can do "{prefox}help <category>" to view the commands.*', color=0xadd8e6)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@help.command(name="config")
async def help_config(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Config Commands', description=f'`{prefox}set-welcome` - Sets the welcome channel and notifies when someone joins. \n \n `{prefox}set-mute` - Sets the mute role which is used in {prefox}mute \n \n `{prefox}set-report` - Sets the report log channel, Usage - **{prefox}set-report <#channel>** \n \n `{prefox}set-suggestion` - Sets the suggestion channel. \n \n `{prefox}links off` - Turns **off** all links and denies links to be sent. \n \n `{prefox}links on` - Turns **on** and allows links to be sent. \n \n `{prefox}verification <on/off/set>` - **On/Off/Set** a verification system. \n \n `{prefox}welcome <on/off/set>` - **On/Off/Set** Welcome Message. \n \n `{prefox}leave <on/off/set>` - **On/Off/Set** Leave Message. \n \n `{prefox}prefix` - Changes the **prefix** of RedSafe on that server.', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="moderation")
async def help_moderation(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Moderation Commands', description='', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="general")
async def help_general(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> General Commands', descrition=f'`{prefox}support` - Gives the link to the **support server**. \n \n `{prefox}invite` - gives a invite that you can use to **invite the bot**. \n \n ', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="staff")
async def help_staff(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Staff Commands', description='', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="music")
async def help_music(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Music Commands', description='', color=0xadd8e6)
    embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="premium")
async def help_premium(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Premium Commands', description='', color=0xff0000)
    embed.set_footer(text='RedSafe Premium', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    before_ws = int(round(client.latency * 1000, 1))
    message = await ctx.send("🏓 Pong!")
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
    embed.add_field(name='Game / Custom Status', value=game, inline=True)
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

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            return m.id

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(self, ctx, member: MemberID, *, reason: str = None):
    """ Bans a user from the current server. """
    m = ctx.guild.get_member(member)
    if m is not None and await permissions.check_priv(ctx, m):
        return

    try:
        await ctx.send(default.actionmessage("banned"))
        audit_logging = discord.utils.get(ctx.guild.channels, name="redsafe-logs")
        embed = discord.Embed(title=":hammer: User Banned: " + str(member.name) + " (" + str(member.id) + ") \n \n Responsible moderator: " + str(ctx.author) + " \n Reason: " + str(reason))
        await audit_logging.send(embed=embed)
        embed2 = discord.Embed(title=f'{ctx.guild.name}', description=f'You have been banned in **{ctx.guild.name}** for : ```{str(reason)}```', color=0xff0000)
        embed2.set_footer(text='RedSafe', icon_url=redsafelogo)
        await member.send(embed=embed2)
        await ctx.guild.ban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
    except Exception as e:
        if "object has no attribute" in str(e):
            await ctx.send("Please make sure to setup a Channel named #redsafe-logs so that I can log mutes / bans. " + ctx.message.author.mention)
        else:
            await ctx.send(e)


@client.command()
@commands.has_permissions(kick_members=True)
async def unban(self, ctx, member: MemberID, *, reason: str = None):
    """ Unbans a user from the current server. """
    try:
        await ctx.guild.unban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
        await ctx.send(default.actionmessage("unbanned"))
        audit_logging = discord.utils.get(ctx.guild.channels, name="redsafe-logs")
        embed = discord.Embed(title=":leaves: User unbanned: " + str(member.name) + " (" + str(member.id) + ") \n \n Responsible moderator: " + str(ctx.author) + " \n Reason: " + str(reason))
        await audit_logging.send(embed=embed)
        embed2 = discord.Embed(title=f'{ctx.guild.name}', description=f'You have been unbanned from **{ctx.guild.name}**', color=0x00ff00)
        embed2.set_footer(text='RedSafe', icon_url=redsafelogo)
        await member.send(embed=embed2)
    except Exception as e:
        if "object has no attribute" in str(e):
            await ctx.send("Please make sure to setup a Channel named #redsafe-logs so that I can log unmutes / unbans. " + ctx.message.author.mention)
        else:
            await ctx.send(e)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, reason=None):
    logs = client.get_channel(LOGGING_CHANNEL)
    if reason == None:
        await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
        embed = discord.Embed(title="Attempt at Kick", color=0x37cdaf)
        embed.add_field(name="Command Issuer", value=ctx.message.author.mention, inline=True)
        embed.add_field(name="Attempted to kick but forgot reason", value=f"{member.name}#{member.discriminator} <@" + str(member.id) + ">" + f"({member.id})", inline=True)
        embed.set_footer(text='RedSafe', icon_url=redsafelogo)
    else:
        memberstr = str(member)
        await logs.send(ctx.message.author.mention + " has kicked person " + memberstr)
        kick = discord.Embed(title="Kick", color=0x37cdaf)
        kick.add_field(name="Moderator", value=ctx.message.author.mention, inline=True)
        kick.add_field(name="Kicked", value=f"{member.name}#{member.discriminator} <@" + str(member.id) + ">" + f"({member.id})", inline=True)
        kick.add_field(name='Reason', value=f'{reason}', inline=True)
        await ctx.send(embed=kick)
        message = f"You have been kicked from {ctx.guild.name} for {reason}"
        await member.send(message)
        await member.kick(reason=f"Moderator:{ctx.message.author.name} Reason:" + reason)



@client.command()
async def honk(ctx):
    await ctx.send("honk")

def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"


client.run(TOKEN)
