import discord
import asyncio
from discord.ext import commands, tasks
import time
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from utils import permissions, default
from discord.utils import get
import re
import os
import youtube_dl
import shutil
from discord.ext.commands import has_permissions, MissingPermissions, errors
import pymongo
from pymongo import MongoClient

#Data Base Below

client = pymongo.MongoClient("mongodb+srv://RedSafe-Bot:F0H5XARYJt69SD9l@redsafe.hoqeu.mongodb.net/RedSafe?retryWrites=true&w=majority")
db = client.RedSafe
client = discord.Client()

#Bot Info below

redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/3f00cd933cf382a9f06212367676e4af.png?size=1024'
TOKEN = "NTQ1MjMwMTM2NjY5MjQxMzY1.XGQXIg.pkMvoANEYVUnbZU-hC9ausZikxE"
bversion = '1.6.2'
devs = '`Benitz Original#1317` and `Kittens#3154`'
botname = 'RedDead'
cmd = '27'
events = '9'

#Prefix below

def prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = prefix)

client.remove_command('help')

#status

status4 = 'You type ".help"'
status2 = 'the Discord API'
status3 = f'{botname} Premium'

async def status_task():
    while True:
        global count
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status4))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status2))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status3))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{count} Servers"))
        await asyncio.sleep(10)



@client.event
async def on_ready():
    before_ws = int(round(client.latency * 1000, 1))
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/760023398838960129/xYvZWgjgv5FpJAjUxaRCmnDovrtECKqSR5MCr-W607QdZ4qmxaAqvegRvQuh5n_U2LjT')
    embed = DiscordEmbed(title='Start-Up', description=f'{client.user} is Online.', color=0x00ff00)
    embed.add_embed_field(name='Bot Name:', value=f'**{client.user}**', inline=True)
    embed.add_embed_field(name='Logged In with ID:', value=f'`{client.user.id}`', inline=True)
    embed.add_embed_field(name='Ping:', value=f'**{before_ws}**ms', inline=True)
    embed.add_embed_field(name=':warning: NOTE! :warning:', value='This Bot is still in **beta stage** and will take a while to release.', inline=False)
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()
    client.loop.create_task(status_task())
    global count

    print('Bot ready')
    print(f"{botname} Active!")
    count = 0
    for guild in client.guilds:
        print("Connected to server: {}".format(guild))
        count +=1

    client.loop.create_task(status_task())

@client.command()
async def rename(ctx, reason: commands.clean_content = None):
    if ctx.author.id == 529499034495483926:
        await client.user.edit(username=reason)

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(self, ctx, *, search: commands.clean_content = None):
    if search == None:
        embed = discord.Embed(title='0 Messages Clear', description='No messages were clear, because you did not spesify the ammount of messages to be deleted.', color=0xff0000)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    else:
        await ctx.channel.purge(limit=int(search))
        embed = discord.Embed(title=f'Messages Cleared', description=f'Specified ammount of messages has been deleted.', color=0x00ff00)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    embed = discord.Embed(title=f'{botname} ShutDown', description='The Bot is being **Shut Down** by the owner, `Benitz Original#1317`', color=0xff0000)
    embed.set_footer(text=f'{botname} ShutDown', icon_url=redsafelogo)
    embed.set_image(url='https://miro.medium.com/max/800/1*TTOJz35-lJmjWGj59786GA.png')
    await ctx.send(embed=embed)
    await client.change_presence(status=discord.Status.offline)
    await ctx.bot.logout()

@client.event
async def on_message(ctx):
    if ctx.content.find(f"<@!{client.user.id}>") != -1:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        embed = discord.Embed(title='> Prefix', description=f"""The current prefix for this server is set to `{prefixes[str(ctx.guild.id)]}`""", color=0x00ff00)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.channel.send(embed=embed)
    await client.process_commands(ctx)

@client.command()
async def invite(ctx):
    embed = discord.Embed(title=f'{botname} Invites', description=f'Here are all the links related to **{botname}** \n\n > [Bot Invite](http://{botname}.bot.nu) \n > [Support Server](https://discord.com/cRTnVaQ) \n > [Website](https://google.com) \n\n This bot is **created**, **managed**, and **developed** by {devs}', color=242424)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.command()
async def about(ctx):

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]

    with open('rspremium.json', 'r') as f:
        rscheck = json.load(f)

    ping = int(round(client.latency * 1000, 1))
    premium = rscheck[str(ctx.guild.id)]
    embed = discord.Embed(title=f'{botname} Bot', description=f'\n**{botname}** is a Powerful Moderation, Staff-Help, Music, Multi-Purpose Bot that you can **[invite](http://{botname}.bot.nu)** and use on **your server**.\n\n :stopwatch:  **Version** - {bversion} \n\n :computer:  **Developers** - {devs} \n\n :key:  **Prefix** - `{prefox}` \n\n :tada:  **Premium** - **{premium}** \n\n :globe_with_meridians:  **Language** - **Discord.py** \n\n :zap:  **Ping** - `{ping}`m/s \n\n :pen_ballpoint: **Commands** - `{cmd}` **Commands Loaded** \n\n :rotating_light: **Events** - `{events}` **Events Loaded**', color=242424)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

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

                with open('prefixes.json', 'r') as f:
                    prefixes = json.load(f)
                prefox = prefixes[str(ctx.guild.id)]

                await message.delete()
                embed = discord.Embed(title=f'{message.guild.name}', description=f"Hey! You aren't allowed swear on **{message.guild.name}** \n\n *If swearing is allowed on this server, please contact a staff member to turn off the swear filter with `{prefox}swear off`*", color=0xff0000)
                embed.set_footer(text=botname, icon_url=redsafelogo)
                await message.author.send(embed=embed)
        else:
            print('')
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
        embed.set_footer(text=f'{Guild.member_count}th Member', icon_url=f'{guild.icon_url}')
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
        embed.set_footer(text=f'{Guild.member_count} Members left', icon_url=f'{guild.icon_url}')
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice.clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f'{botname} has Joined {channel}')

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'{botname} has disconnected from {channel}')
    else:
        await ctx.send(f"{botname} isn't connected to any Voice Channels.")

@client.command()
async def bc(ctx):
    await ctx.send('<info:>')

@client.group()
@commands.has_permissions(administrator=True)
async def suggestion(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='Suggestion', description=f'You can turn **on**, **off**, or **set** Suggestion Channels. \n Usage: \n \n `{prefix}suggestion on` - Turns on the Suggestion Module. \n `{prefix}suggestion off` - Turns off the Suggestion Module. \n `{prefix}suggesion set <#channel>` - Set the Suggesiton channel.', color=0x00ff00)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@suggestion.command(name='set')
async def suggetion_set(ctx, string):

    with open('suggestcha.json', 'r') as f:
        channel = json.load(f)

    schannel = int(re.search(r'\d+', string).group(0))

    channel[str(ctx.guild.id)] = schannel

    with open('suggestcha.json', 'w') as f:
        json.dump(channel, f, indent=4)

    embed = discord.Embed(title='Suggestion Channel', description=f'The Suggestion Channel been set to {string}', color=0x00ff00)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@suggestion.command(name='on')
async def suggestion_on(ctx):
    with open('suggestset.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "enabled"

    with open('suggestset.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Suggestion', description=f'The Suggestion Module has been **Enabled**', color=0x00ff00)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)




#Warn command
@client.command()
@has_permissions(kick_members=True)
async def warn(ctx, member:discord.Member, *, reason=None):
    arg=reason
    author=ctx.author
    guild=ctx.message.guild
    overwritee = discord.PermissionOverwrite()
    overwrite = discord.PermissionOverwrite()
    channel = get(guild.text_channels, name='warn-logs')

    if channel is None:
        channel = await guild.create_text_channel('warn-logs')
        overwritee.read_messages = False
        overwritee.read_message_history = False
        overwritee.send_messages = False
        overwrite.read_messages = True
        overwrite.read_message_history = True
        overwrite.send_messages = True
        await channel.set_permissions(guild.default_role, overwrite=overwritee)

    if member is None:
        await ctx.send("Please specify a user and/or reason!")

        await channel.send(f'{member.mention} got warned for: ```\n{arg}\n``` Warned by: {author.mention}')
        await member.send(f'You got warned for: ```\n{arg}\n``` Warned by: {author} Warned on: **{guild.name}**')
        await ctx.send(f'{member.mention} got warned for: ```\n{arg}\n``` Warned by: {author.mention}')
        await ctx.message.delete()

@client.command()
async def suggest(ctx, *, reason: commands.clean_content = None):
    with open('suggestcha.json', 'r') as f:
        prefixes = json.load(f)

    prefix = prefixes[str(channel.guild.id)]

    with open('suggestset.json', 'r') as f:
        suggest = json.load(f)

    suggest = joe[str(channel.guild.id)]
    if suggest == 'enabled':
        embed = discord.Embed(title='Suggestion', description=f'Suggestion from {ctx.author.name} -  \n \n {reason}')
        chnl = client.get_channel(int(prefix))
        await chnl.send(embed=embed)

@client.group()
@commands.has_permissions(administrator=True)
async def swear(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='Swear Filter', description=f'You can turn **on**, or **off** the Swear Filter if you have {botname} Premium. \n Usage: \n \n `{prefix}swear on` - Turns on the Swear Filter. \n `{prefix}swear off` - Turns off the Swear Filter.', color=0x00ff00)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await ctx.send(embed=embed)

@client.command()
async def bug(ctx, *, reason: commands.clean_content = None):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    if reason:
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758644853441298462/VTSA8bQ797HENYiQnhphnWpalE3UJHmod4tu27HjThs6HZl6pgIQLvtxCE1h1AyaJqMu')
        embed = DiscordEmbed(title=f'New Bug from {ctx.author.name}', description=f'Bug - \n \n {reason}', color=242424)
        embed.set_footer(text=f'{ctx.guild.name} | {ctx.guild.id}', icon_url=redsafelogo)
        webhook.add_embed(embed)
        webhook.execute()
        rs = discord.Embed(title=f'{botname} Bugs', description=f'The bug has been reported to {botname} Developers. Thank you for reporting the bug.\n You can join {botname} support with `{prefox}invite`', color=0x00ff00)
        rs.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.send(embed=rs)
        time.sleep(10)
        await client.delete_message(message)
    else:
        nos = discord.Embed(title=f'{botname} Bugs', description=f"You have to do `{prefox}bug <bugreport>` to send a bug, `{prefox}bug` doesn't do anything.\n No report has been sent to the Developers.", color=0xff0000)
        nos.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.send(embed=nos)
        time.sleep(10)
        await client.delete_message(message)

@swear.command(name="on")
@commands.has_permissions(administrator=True)
async def swear_on(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]

    with open('rspremium.json', 'r') as f:
        rscheck = json.load(f)
    premium = rscheck[str(ctx.guild.id)]

    if premium == 'enabled':
        with open('swearfilterboi.json', 'r') as f:
            verify = json.load(f)

        verify[str(ctx.guild.id)] = "enabled"

        with open('swearfilterboi.json', 'w') as f:
            json.dump(verify, f, indent=4)

        embed = discord.Embed(title='Swear Filter', description=f'The Swear Filter has been **Enabled**', color=0x00ff00)
        embed.set_footer(text=f'{botname} Premium', icon_url=redsafelogo)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f'{botname} Premium', description=f"You don't have {botname} Premium active. \n You can activate it from the support server. \n You can get the Support Server invite link by doing `{prefox}invite`")
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@swear.command(name="off")
@commands.has_permissions(administrator=True)
async def swear_off(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]

    with open('rspremium.json', 'r') as f:
        rscheck = json.load(f)
    premium = rscheck[str(ctx.guild.id)]

    if premium == 'enabled':

        with open('swearfilterboi.json', 'r') as f:
            verify = json.load(f)

            verify[str(ctx.guild.id)] = "disabled"

            with open('swearfilterboi.json', 'w') as f:
                json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Swear Filter', description=f'The Swear Filter has been **Disabled**', color=0x00ff00)
    embed.set_footer(text=f'{botname} Premium', icon_url=redsafelogo)
    await ctx.send(embed=embed)






@client.group()
@commands.has_permissions(administrator=True)
async def welcome(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title=f'{botname} Welcome', description=f'You can turn **on**, **off**, or **set** Welcome message. \n Usage: \n \n `{prefix}welcome on` - Turns on the Welcome Messages. \n `{prefix}welcome off` - Turns off the Welcome Messages. \n `{prefix}welcome set <#channel>` - Set the welcome channel.', color=0x00ff00)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@welcome.command(name="on")
@commands.has_permissions(administrator=True)
async def welcome_on(ctx):

    with open('onjoinconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "enabled"

    with open('onleaveconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title=f'{botname} Welcome', description=f'Welcome Message has been **Enabled**', color=0x00ff00)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@welcome.command(name="off")
@commands.has_permissions(administrator=True)
async def welcome_off(ctx):

    with open('onjoinconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('onjoinconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title=f'{botname} Welcome', description=f'Welcome Message has been **Disabled**', color=0xff0000)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
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

    embed = discord.Embed(title=f'{botname} Welcome', description=f'The Welcome Channel been set to {string}', color=0x00ff00)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.group()
@commands.has_permissions(administrator=True)
async def leavemsg(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title=f'{botname} leave', description=f'You can turn **on**, **off**, or **set** leave message. \n Usage: \n \n `{prefix}leave on` - Turns on the leave Messages. \n `{prefix}leave off` - Turns off the leave Messages. \n `{prefix}leave set <#channel>` - Set the leave channel.', color=0x00ff00)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@leavemsg.command(name="on")
@commands.has_permissions(administrator=True)
async def leavemsg_on(ctx):

    with open('onleaveconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "enabled"

    with open('onleaveconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Leave Message', description=f'The Leave Message has been **Enabled**', color=0x00ff00)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@leavemsg.command(name="off")
@commands.has_permissions(administrator=True)
async def leavemsg_off(ctx):

    with open('onleaveconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('onleaveconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Leave Message', description=f'The Leave Message has been **Disabled**', color=0xff0000)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@leavemsg.command(name="set")
@commands.has_permissions(administrator=True)
async def leavemsg_set(ctx, string):

    with open('onleaveconfigset.json', 'r') as f:
        verify = json.load(f)

    boop = int(re.search(r'\d+', string).group(0))

    verify[str(ctx.guild.id)] = boop

    with open('onleaveconfigset.json', 'w') as f:
        json.dump(verify, f, indent=4)

    embed = discord.Embed(title='Leave Message', description=f'The Leave Message Channel been set to {string}', color=0x00ff00)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
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
       embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
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
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.event
async def on_guild_join(guild):
    global count
    count +=1

    with open('swearfilterboi.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('swearfilterboi.json', 'w') as f:
        json.dump(verify, f, indent=4)

    with open('onjoinconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('onjoinconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    with open('onleaveconfig.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('onleaveconfig.json', 'w') as f:
        json.dump(verify, f, indent=4)

    with open('verifysetting.json', 'r') as f:
        verify = json.load(f)

    verify[str(ctx.guild.id)] = "disabled"

    with open('verifysetting.json', 'w') as f:
        json.dump(verify, f, indent=4)

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    with open('prefixes.json', 'r') as f:
        rspre = json.load(f)

    rspre[str(ctx.guild.id)] = 'disabled'

    with open('prefixes.json', 'w') as f:
        json.dump(rspre, f, indent=4)

    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/758248651515625503/r4JCjSTWZ9ly3sxnYjzjzF3g1saIgEqGY_cXxg6hmexnnhcokk_IM1qm138li0Judg2p')
    embed = DiscordEmbed(title='New Guild Join!', description=f"Guild : {guild.name} \n \n ID : {guild.id} \n \n Owner : {guild.owner}", color=242424)
    webhook.add_embed(embed)
    webhook.execute()
    embed = discord.Embed(title=f'{botname}', description='Hello There, This is RebootSafe. \n My prefix default is `.` You can change it with `.prefix set {prefix}` \n Have a nice day!', color=0xFFA500)
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
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
@commands.cooldown(1, 300, commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def notify(ctx, user_id: int, *, message: str):
    """ DM the user of your choice """
    user = client.get_user(user_id)
    if not user:
        return await ctx.send(f"Could not find any UserID matching **{user_id}**")

    try:
        embed = discord.Embed(title=f"{ctx.guild.name}", description=f"New message from **{ctx.guild.name}**'s Staff \n \n  Message - {message}", color=0x1868af)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await user.send(embed=embed)
        await ctx.send(f"**{user_id}** has been notified, followed by the message.")
    except discord.Forbidden:
        await ctx.send("Unable to notify user, user may have DMs closed or, User might be a bot.")

@client.event
async def on_command_error(ctx, err):
    if isinstance(err, errors.CommandOnCooldown):
        await ctx.send(f"Command is on Cooldown, please try again in {err.retry_after:.2f} seconds.")
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
        return await ctx.send('Error: `no "Muted" role found.`')

    try:
        await member.add_roles(muted_role, reason=default.responsible(ctx.author, reason))
        await ctx.send(default.actionmessage("muted"))
        audit_logging = discord.utils.get(ctx.guild.channels, name="redsafe-logs")
        embed = discord.Embed(title='User has been muted', description=":mute: User muted: " + str(member.name) + " (" + str(member.id) + ") \n \n Responsible moderator: " + str(ctx.author) + " \n Reason: " + str(reason), color=0xff0000)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await audit_logging.send(embed=embed)
        embed2 = discord.Embed(title=f'{ctx.guild.name}', description=f'You have been muted in **{ctx.guild.name}** for : ```{str(reason)}```', color=0xff0000)
        embed2.set_footer(text=f'action by {author.name} | {botname}', icon_url=redsafelogo)
        await member.send(embed=embed2)
    except Exception as e:
        if "object has no attribute" in str(e):
            await ctx.send('`Error: No "#redsafe-logs" log channel found`')
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
        return await ctx.send('Error: `no "Muted" role found.`')

    try:
        await member.remove_roles(muted_role, reason=default.responsible(ctx.author, reason))
        await ctx.send(default.actionmessage("unmuted"))
        audit_logging = discord.utils.get(ctx.guild.channels, name="redsafe-logs")
        embed = discord.Embed(title='User has been unmuted', description=":loud_sound: User unmuted: " + str(member.name) + " (" + str(member.id) + ") \n \n Responsible moderator: " + str(ctx.author) + " \n Reason: " + str(reason))
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await audit_logging.send(embed=embed)
        embed2 = discord.Embed(title=f'{ctx.guild.name}', description=f'You have been unmuted in **{ctx.guild.name}**', color=0x00ff00)
        embed2.set_footer(text=f'action by {author.name} | {botname}', icon_url=redsafelogo)
        await member.send(embed=embed2)
    except Exception as e:
        if "object has no attribute" in str(e):
            await ctx.send('`Error: No "#redsafe-logs" log channel found`')
        else:
            await ctx.send(e)

@client.group()
async def premium(ctx):
    if ctx.invoked_subcommand is None:
        print("boop")

@premium.command(name="check")
async def premium_check(ctx):
        with open('rspremium.json', 'r') as f:
            rscheck = json.load(f)

        premium = rscheck[str(ctx.guild.id)]
        embed = discord.Embed(title=f'{botname} Premium', description=f'{botname} Premium is currently {premium}', color=0x00ff00)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
        await ctx.send(embed=embed)

@client.group()
@commands.has_permissions(administrator=True)
async def verification(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title='Verification', description=f'You can turn **on**, **off**, or **set** verified roles \n Usage: \n \n `{prefix}verification on` - Turns the verification system on. \n `{prefix}verification off` - Turns off the verification system. \n `{prefix}verification set <@role>` - sets a role that is given after verification.', color=0x00ff00)
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
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
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
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
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
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
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
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
        embed.set_footer(text=f'{botname}', icon_url=redsafelogo)

        user = client.get_user(ctx.author.id)
        await user.send(embed=embed)

    else:
        print(f'Verification not enabled on {guild.name}.')

@client.command()
async def avatar(ctx, *, user: discord.Member = None):
    """ Get the avatar of you or someone else """
    user = user or ctx.author
    embed = discord.Embed(title=f"{user.name}'s avatar", color=0x00ff00)
    embed.set_image(url=user.avatar_url_as(size=1024))
    embed.set_footer(text=f'{botname}', icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title="> Command Categories", description=f'`config` - Config Commands \n `moderation` - Moderation Commands \n `general` - General commands anyone can use. \n `staff` - Commands that will help the staff members. \n `music` - Music Commands! \n `premium` - **Premium** Commands that will only work if you get **premium**. \n \n *You can do "{prefox}help <category>" to view the commands.*', color=0xadd8e6)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await ctx.send(embed=embed)

@help.command(name="config")
async def help_config(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Config Commands', description=f'`{prefox}set-welcome` - Sets the welcome channel and notifies when someone joins. \n \n `{prefox}set-mute` - Sets the mute role which is used in {prefox}mute \n \n `{prefox}set-report` - Sets the report log channel, Usage - **{prefox}set-report <#channel>** \n \n `{prefox}set-suggestion` - Sets the suggestion channel. \n \n `{prefox}links off` - Turns **off** all links and denies links to be sent. \n \n `{prefox}links on` - Turns **on** and allows links to be sent. \n \n `{prefox}verification <on/off/set>` - **On/Off/Set** a verification system. \n \n `{prefox}welcome <on/off/set>` - **On/Off/Set** Welcome Message. \n \n `{prefox}leave <on/off/set>` - **On/Off/Set** Leave Message. \n \n `{prefox}prefix` - Changes the **prefix** of RedSafe on that server.', color=0xadd8e6)
    embed.set_footer(text=botname, icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="moderation")
async def help_moderation(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Moderation Commands', description=f'`{prefox}kick` - **kicks** and **notifies** the mentioned User. \n\n `{prefox}ban` - **Bans** and **notifes** the mentioned User. \n\n `{prefox}mute` - Mutes the mentioned user permanently *(still in progress)*', color=0xadd8e6)
    embed.set_footer(text=botname, icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="general")
async def help_general(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> General Commands', descrition=f'`{prefox}ping` - Shows the Webshock and Rest latency of the bot. \n\n `{prefox}invite` - Provides all the **links** that is related to {botname}. \n \n ', color=0xadd8e6)
    embed.set_footer(text=botname, icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="staff")
async def help_staff(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Staff Commands', description=f'`{prefox}notify` - Notifies the user with the message sent by the staff. \n\n `{prefox}clear` - Clears a specified ammount of messages. \n\n ', color=0xadd8e6)
    embed.set_footer(text=botname, icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="music")
async def help_music(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Music Commands', description=f"Sorry, {botname}'s Music Commands aren't ready.", color=0xadd8e6)
    embed.set_footer(text=botname, icon_url=redsafelogo)
    await ctx.send(embed=embed)

@help.command(name="premium")
async def help_premium(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefox = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='> Premium Commands', description=f"Sorry, {botname}'s Premium Commands aren't ready.", color=0xff0000)
    embed.set_footer(text=botname, icon_url=redsafelogo)
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
    embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
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
    embed.set_footer(text=botname, icon_url=redsafelogo)
    await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)
    emoji_count = len(ctx.guild.emojis)
    channel_count = len([x for x in ctx.guild.channels if isinstance(x, discord.channel.TextChannel)])
    embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
    embed.add_field(name='Server (ID)', value=f"{ctx.guild.name} ({ctx.guild.id})")
    embed.add_field(name='Server Owner', value=ctx.guild.owner, inline=False)
    embed.add_field(name='Member Count', value=ctx.guild.member_count)
    embed.add_field(name='Text Channels', value=str(channel_count))
    embed.add_field(name='Region', value=ctx.guild.region)
    embed.add_field(name='Verification Level', value=str(ctx.guild.verification_level))
    embed.add_field(name='Highest role', value=ctx.guild.roles[-1])
    embed.add_field(name='Number of roles', value=str(role_count))
    embed.add_field(name='Number of emotes', value=str(emoji_count))
    embed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=botname, icon_url=redsafelogo)
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
        embed = discord.Embed(title='Banned User', description=":hammer: User Banned: " + str(member.name) + " (" + str(member.id) + ") \n \n Responsible moderator: " + str(ctx.author) + " \n Reason: " + str(reason), color=0xff0000)
        await audit_logging.send(embed=embed)
        embed2 = discord.Embed(title=f'{ctx.guild.name}', description=f'You have been banned in **{ctx.guild.name}** for : ```{str(reason)}```', color=0xff0000)
        embed2.set_footer(text=botname, icon_url=redsafelogo)
        await member.send(embed=embed2)
        await ctx.guild.ban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
    except Exception as e:
        if "object has no attribute" in str(e):
            await ctx.send('`Error: No "#redsafe-logs" log channel found`')
        else:
            await ctx.send(e)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(self, ctx, member: MemberID, *, reason: str = None):
    """ Unbans a user from the current server. """
    try:
        await ctx.guild.unban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
        await ctx.send(default.actionmessage("unbanned"))
        audit_logging = discord.utils.get(ctx.guild.channels, name="redsafe-logs")
        embed = discord.Embed(title='Unbanned User', description=":leaves: User unbanned: " + str(member.name) + " (" + str(member.id) + ") \n \n Responsible moderator: " + str(ctx.author) + " \n Reason: " + str(reason), color=0x00ff00)
        await audit_logging.send(embed=embed)
        embed2 = discord.Embed(title=f'{ctx.guild.name}', description=f'You have been unbanned from **{ctx.guild.name}**', color=0x00ff00)
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await member.send(embed=embed2)
    except Exception as e:
        if "object has no attribute" in str(e):
            await ctx.send('`Error: No "#redsafe-logs" log channel found`')
        else:
            await ctx.send(e)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, reason=None):
    logs = client.get_channel(LOGGING_CHANNEL)
    if reason == None:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefox = prefixes[str(ctx.guild.id)]

        await ctx.send(f"Incorrect Usage, try **{prefox}kick <@user> <reason>**")
        embed = discord.Embed(title="Attempt at Kick", color=0x37cdaf)
        embed.add_field(name="Command Issuer", value=ctx.message.author.mention, inline=True)
        embed.add_field(name="Attempted to kick but forgot reason", value=f"{member.name}#{member.discriminator} <@" + str(member.id) + ">" + f"({member.id})", inline=True)
        embed.set_footer(text=botname, icon_url=redsafelogo)
    else:
        memberstr = str(member)
        await logs.send(ctx.message.author.mention + " has kicked person " + memberstr)
        kick = discord.Embed(title="Kick", color=0x37cdaf)
        kick.add_field(name="Moderator", value=ctx.message.author.mention, inline=True)
        kick.add_field(name="Kicked", value=f"{member.name}#{member.discriminator} <@" + str(member.id) + ">" + f"({member.id})", inline=True)
        kick.add_field(name='Reason', value=f'{reason}', inline=True)
        kick.set_footer(text=botname, icon_url=redsafelogo)
        await ctx.send(embed=kick)
        embed = discord.Embed(title=f'{ctx.guild.name}', description=f"You've been kicked from {ctx.guild.name}")
        embed.set_footer(text=botname, icon_url=redsafelogo)
        await member.send(embed=embed)
        await member.kick(reason=f"Moderator:{ctx.message.author.name} Reason:" + reason)



@client.command()
async def honk(ctx):
    await ctx.send("honk")

def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"


client.run(TOKEN, bot = True, reconnect = True)
