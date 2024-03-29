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
import asyncio
import functools
import itertools
import math
import random
import os
import pymongo

import discord
import youtube_dl

from pymongo import MongoClient
from discord.utils import get
from utils import default
from async_timeout import timeout
from discord.ext import commands

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

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''

config = default.get("./config.json")

class CustomCommand(commands.Command):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.perms = kwargs.get("perms", None)
        self.syntax = kwargs.get("syntax", None)

class VoiceError(Exception):
	pass


class YTDLError(Exception):
	pass


class YTDLSource(discord.PCMVolumeTransformer):
	YTDL_OPTIONS = {
		'format': 'bestaudio/best',
		'extractaudio': True,
		'audioformat': 'mp3',
		'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
		'restrictfilenames': True,
		'noplaylist': True,
		'nocheckcertificate': True,
		'ignoreerrors': False,
		'logtostderr': False,
		'quiet': True,
		'no_warnings': True,
		'default_search': 'auto',
		'source_address': '0.0.0.0',
	}

	FFMPEG_OPTIONS = {
		'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
		'options': '-vn',
	}

	ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

	def __init__(self, ctx, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
		super().__init__(source, volume)

		self.requester = ctx.author
		self.channel = ctx.channel
		self.data = data

		self.uploader = data.get('uploader')
		self.uploader_url = data.get('uploader_url')
		date = data.get('upload_date')
		self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
		self.title = data.get('title')
		self.thumbnail = data.get('thumbnail')
		self.description = data.get('description')
		self.duration = self.parse_duration(int(data.get('duration')))
		self.tags = data.get('tags')
		self.url = data.get('webpage_url')
		self.views = data.get('view_count')
		self.likes = data.get('like_count')
		self.dislikes = data.get('dislike_count')
		self.stream_url = data.get('url')

	def __str__(self):
		return '**{0.title}** by **{0.uploader}**'.format(self)

	@classmethod
	async def create_source(cls, ctx, search: str, *, loop: asyncio.BaseEventLoop = None):
		loop = loop or asyncio.get_event_loop()

		partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
		data = await loop.run_in_executor(None, partial)

		if data is None:
			raise YTDLError(f'{config.forbidden} Couldn\'t find anything that matches' + '`{}`'.format(search))

		if 'entries' not in data:
			process_info = data
		else:
			process_info = None
			for entry in data['entries']:
				if entry:
					process_info = entry
					break

			if process_info is None:
				raise YTDLError(f'{config.forbidden} Couldn\'t find anything that matches' + '`{}`'.format(search))

		webpage_url = process_info['webpage_url']
		partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
		processed_info = await loop.run_in_executor(None, partial)

		if processed_info is None:
			raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

		if 'entries' not in processed_info:
			info = processed_info
		else:
			info = None
			while info is None:
				try:
					info = processed_info['entries'].pop(0)
				except IndexError:
					raise YTDLError(f'{config.forbidden} Couldn\'t find anything that matches' + '`{}`'.format(search))

		return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

	@staticmethod
	def parse_duration(duration: int):
		minutes, seconds = divmod(duration, 60)
		hours, minutes = divmod(minutes, 60)
		days, hours = divmod(hours, 24)

		duration = []
		if days > 0:
			duration.append('{} days'.format(days))
		if hours > 0:
			duration.append('{} hours'.format(hours))
		if minutes > 0:
			duration.append('{} minutes'.format(minutes))
		if seconds > 0:
			duration.append('{} seconds'.format(seconds))

		return ', '.join(duration)


class Song:
	__slots__ = ('source', 'requester')

	def __init__(self, source: YTDLSource):
		self.source = source
		self.requester = source.requester

	def create_embed(self):
		embed = discord.Embed(color=242424)
		embed.set_author(name="Playing", icon_url=self.requester.display_avatar)
		embed.add_field(name="Song:", value=f"[{self.source.title}]({self.source.url}) by [{self.source.uploader}]({self.source.uploader_url})")
		embed.add_field(name='Duration:', value=f"`{self.source.duration}`", inline=False)
		embed.add_field(name='Requested by:', value=self.requester.mention, inline=False)
		embed.set_footer(text="Numix Music", icon_url=config.logo)

		return embed


class SongQueue(asyncio.Queue):
	def __getitem__(self, item):
		if isinstance(item, slice):
			return list(itertools.islice(self._queue, item.start, item.stop, item.step))
		else:
			return self._queue[item]

	def __iter__(self):
		return self._queue.__iter__()

	def __len__(self):
		return self.qsize()

	def clear(self):
		self._queue.clear()

	def shuffle(self):
		random.shuffle(self._queue)

	def remove(self, index: int):
		del self._queue[index]


class VoiceState:
	def __init__(self, bot: commands.AutoShardedBot, ctx):
		self.bot = bot
		self._ctx = ctx

		self.current = None
		self.voice = None
		self.next = asyncio.Event()
		self.songs = SongQueue()

		self._loop = False
		self._volume = 0.5
		self.skip_votes = set()

		self.audio_player = bot.loop.create_task(self.audio_player_task())

	def __del__(self):
		self.audio_player.cancel()

	@property
	def loop(self):
		return self._loop

	@loop.setter
	def loop(self, value: bool):
		self._loop = value

	@property
	def volume(self):
		return self._volume

	@volume.setter
	def volume(self, value: float):
		self._volume = value

	@property
	def is_playing(self):
		return self.voice and self.current

	async def audio_player_task(self):
		while True:
			self.next.clear()

			if not self.loop:
				try:
					async with timeout(180):  # 3 minutes
						self.current = await self.songs.get()
				except asyncio.TimeoutError:
					self.bot.loop.create_task(self.stop())
					return

			self.current.source.volume = self._volume
			self.voice.play(self.current.source, after=self.play_next_song)
			await self.current.source.channel.send(embed=self.current.create_embed())

			await self.next.wait()

	def play_next_song(self, error=None):
		if error:
			raise VoiceError(str(error))

		self.next.set()

	def skip(self):
		self.skip_votes.clear()

		if self.is_playing:
			self.voice.stop()

	async def stop(self):
		self.songs.clear()

		if self.voice:
			await self.voice.disconnect()
			self.voice = None


class music(commands.Cog):
	def __init__(self, bot: commands.AutoShardedBot):
		self.bot = bot
		self.voice_states = {}

	def get_voice_state(self, ctx):
		state = self.voice_states.get(ctx.guild.id)
		if not state:
			state = VoiceState(self.bot, ctx)
			self.voice_states[ctx.guild.id] = state

		return state

	def cog_unload(self):
		for state in self.voice_states.values():
			self.bot.loop.create_task(state.stop())

	def cog_check(self, ctx):
		if not ctx.guild:
			raise commands.NoPrivateMessage(f'{config.forbidden} This command can\'t be used in DMs.')

		return True

	async def cog_before_invoke(self, ctx):
		ctx.voice_state = self.get_voice_state(ctx)

	async def cog_command_error(self, ctx, error: commands.CommandError):
		await ctx.send(f'{config.forbidden}' + '{}'.format(str(error)))

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!join", invoke_without_subcommand=True,description="Joins a voice channel")
	async def join(self, ctx):
		"""Joins a voice channel."""

		destination = ctx.author.voice.channel
		if ctx.voice_state.voice:
			await ctx.voice_state.voice.move_to(destination)
			
			return

		ctx.voice_state.voice = await destination.connect()
		await ctx.send(f'{config.success} Joined the Voice Channel.')

	@commands.command(cls=CustomCommand, perms="MANAGE_GUILD", syntax="n!summon [channel]", description='Summons the bot to a voice channel', aliases=["smn"])
	@permission("manage_guild")
	async def summon(self, ctx, *, channel: discord.VoiceChannel = None):
		"""Summons the bot to a voice channel.

		If no channel was specified, it joins your channel.
		"""

		if not channel and not ctx.author.voice:
			raise VoiceError(f'{config.forbidden} You are currently not connected to any voice channel.')

		destination = channel or ctx.author.voice.channel
		if ctx.voice_state.voice:
			await ctx.voice_state.voice.move_to(destination)
			return

		ctx.voice_state.voice = await destination.connect()
		await ctx.send(f'{config.success} Bot summoned!')

	@commands.command(cls=CustomCommand, perms="MANAGE_GUILD", syntax="n!leave", aliases=['disconnect'],description="Clear the queue and leave any voice channel")
	@permission("manage_guild")
	async def leave(self, ctx):
		"""Clears the queue and leaves the voice channel."""
		if not ctx.voice_state.voice:
			return await ctx.send(f'{config.forbidden} Not connected to any voice channels.')

		await ctx.voice_state.stop()
		del self.voice_states[ctx.guild.id]

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!np", aliases=['current', 'playing'],description='Shows current song')
	async def np(self, ctx):
		"""Displays the currently playing song."""

		await ctx.send(embed=ctx.voice_state.current.create_embed())

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!pause", description='Pause the current song')
	async def pause(self, ctx):
		"""Pauses the currently playing song."""

		if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
			ctx.voice_state.voice.pause()
			await ctx.message.add_reaction('⏯')
		else:
			await ctx.send(f"{config.forbidden} No music playing.")

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!resume", description='Resume the paused song')
	async def resume(self, ctx):
		"""Resumes a currently paused song."""

		if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
			ctx.voice_state.voice.resume()
			await ctx.message.add_reaction('⏯')
		else:
			await ctx.send(f"{config.forbidden} Music not paused.")


	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!stop", description='Stops playing the song and clears the queue')
	async def stop(self, ctx):
		"""Stops playing song and clears the queue."""

		ctx.voice_state.songs.clear()

		if ctx.voice_state.is_playing:
			ctx.voice_state.voice.stop()
			await ctx.message.add_reaction('⏹')

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!skip", description='Vote to skip the song')
	async def skip(self, ctx):
		"""Vote to skip a song. The requester can automatically skip.
		3 skip votes are needed for the song to be skipped.
		"""
		if ctx.author.guild_permissions.manage_messages:

			if not ctx.voice_state.is_playing:
				return await ctx.send(f'{config.forbidden} No music playing.')

			ctx.voice_state.skip()

		else:

			if not ctx.voice_state.is_playing:
				return await ctx.send(f'{config.forbidden} No music playing.')

			voter = ctx.message.author
			if voter == ctx.voice_state.current.requester:
				await ctx.message.add_reaction('⏭')
				ctx.voice_state.skip()

			elif voter.id not in ctx.voice_state.skip_votes:
				ctx.voice_state.skip_votes.add(voter.id)
				total_votes = len(ctx.voice_state.skip_votes)

				if total_votes >= 3:
					await ctx.message.add_reaction('⏭')
					ctx.voice_state.skip()
				else:
					await ctx.send(f'{config.success} Skip vote added,' + ' **{}/3**'.format(total_votes))

			else:
				await ctx.send(f'{config.forbidden} You already voted to skip.')

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!queue [page]", description='Shows the player queue')
	async def queue(self, ctx, *, page: int = 1):

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send(f'{config.forbidden} Empty queue.')

		items_per_page = 10
		pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

		start = (page - 1) * items_per_page
		end = start + items_per_page

		queue = ''
		for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
			queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

		embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
				 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
		await ctx.send(embed=embed)

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!shuffle", description='Shuffle the playing song')
	async def shuffle(self, ctx):
		"""Shuffles the queue."""

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send(f'{config.forbidden} The queue is Empty.')

		ctx.voice_state.songs.shuffle()
		await ctx.message.add_reaction(f'{config.success}')

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!remove [index]", description='Remove the song from queue', aliases=["rm"])
	async def remove(self, ctx, index: int):
		"""Removes a song from the queue at a given index."""

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send(f'{config.forbidden} The queue is Empty.')

		ctx.voice_state.songs.remove(index - 1)
		await ctx.message.add_reaction(f'{config.success}')

	@commands.command(cls=CustomCommand, perms="@everyone", syntax="n!play <song name>", description='Plays the given song', aliases=["p", "pl", "pla"])
	async def play(self, ctx, *, search: str):

		if not ctx.voice_state.voice:
			destination = ctx.author.voice.channel
			if ctx.voice_state.voice:
				await ctx.voice_state.voice.move_to(destination)

			else:
				ctx.voice_state.voice = await destination.connect()

		async with ctx.typing():
			try:
				source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
			except YTDLError as e:
				await ctx.send('{}'.format(str(e)))
			else:
				song = Song(source)

				await ctx.voice_state.songs.put(song)
				await ctx.send(f"{config.success} Song added to queue.")

	@join.before_invoke
	@play.before_invoke
	async def ensure_voice_state(self, ctx):
		if not ctx.author.voice or not ctx.author.voice.channel:
			raise commands.CommandError(f'{config.forbidden} You are currently not connected to any voice channel.')

		if ctx.voice_client:
			if ctx.voice_client.channel != ctx.author.voice.channel:
				raise commands.CommandError(f'{config.forbidden} Already in a voice channel.')


async def setup(bot):
	await bot.add_cog(music(bot))
