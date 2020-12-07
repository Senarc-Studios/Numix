import time
import discord
import psutil
import os
import json
import pymongo

from discord.utils import get
from datetime import datetime
from discord.ext import commands
from utils import default
from pymongo import MongoClient

#DB
cluster = MongoClient('mongodb+srv://RedSafe-Bot:F0H5XARYJt69SD9l@redsafe.hoqeu.mongodb.net/RedSafe?retryWrites=true&w=majority')
db = cluster['RedSafe']
#DB

#meta data
redsafelogo = 'https://cdn.discordapp.com/avatars/545230136669241365/af33e499779a7f1f8dfad17b4bf72497.png?size=1024'
bversion = '2.2.1'
devs = '`Danoxzilla-X#7003`, `Benitz Original#1317` and `MythicalKittens#0001`'
botname = 'RedSafe'
cmd = '27'
events = '9'
#meta data

class Filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        with open('sfilter.json', 'r') as f:
			swearfilter = json.load(f)
		filterconfig = swearfilter[str(ctx.guild.id)]
        
        if filterconfig == "enabled":
            
            user = message.author
			
            blocked_words = ["f**k", "fuk", "fuc", "fuck", "f*ck", "bitch", "b*tch", "n*gga", "ni**a", "nigga", "vegina", "fag", "f*g", "dick", "d*ck", "penis", "porn", "sex", "s*x", "hentai", "henti", "pxrn", "p*rn", "a$$", "cunt", "c*nt", "boob", "tits", "cock", "f u c k", "s h i t", "b i t c h", "h e n t a i", "p o r n", "d!ck"]
			
            for x in blocked_words:
				if x in message.content.lower():
					await message.delete()
					blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained a Blocked Words, you may delete the blocked word and send the message again.', color=0xF26A72)
					blocked_word.set_footer(text='Discord.py For Beginners', icon_url=logo)
					await user.send(embed=blocked_word)				
			await bot.process_commands(message)

def setup(bot):
    bot.add_cog(Filter(bot))