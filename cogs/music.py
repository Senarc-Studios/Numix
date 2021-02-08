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

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''

config = default.get("./config.json")

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

	def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
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
	async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
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
		embed = discord.Embed(description='```css\n{0.source.title}\n```'.format(self), color=242424)
		embed.set_author(name="Now Playing", icon_url=self.requester.avatar_url)
		embed.add_field(name='Duration:', value=self.source.duration)
		embed.add_field(name='Requested by:', value=self.requester.mention)
		embed.add_field(name='Uploader:', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
		embed.add_field(name='YouTube URL:', value='{0.source.url}'.format(self))
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
	def __init__(self, bot: commands.AutoShardedBot, ctx: commands.Context):
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


class Music(commands.Cog):
	def __init__(self, bot: commands.AutoShardedBot):
		self.bot = bot
		self.voice_states = {}

	def get_voice_state(self, ctx: commands.Context):
		state = self.voice_states.get(ctx.guild.id)
		if not state:
			state = VoiceState(self.bot, ctx)
			self.voice_states[ctx.guild.id] = state

		return state

	def cog_unload(self):
		for state in self.voice_states.values():
			self.bot.loop.create_task(state.stop())

	def cog_check(self, ctx: commands.Context):
		if not ctx.guild:
			raise commands.NoPrivateMessage(f'{config.forbidden} This command can\'t be used in DMs.')

		return True

	async def cog_before_invoke(self, ctx: commands.Context):
		ctx.voice_state = self.get_voice_state(ctx)

	async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
		await ctx.send(f'{config.forbidden}' + '{}'.format(str(error)))

	@commands.command(invoke_without_subcommand=True,description="Joins a voice channel")
	async def join(self, ctx: commands.Context):
		"""Joins a voice channel."""

		destination = ctx.author.voice.channel
		if ctx.voice_state.voice:
			await ctx.voice_state.voice.move_to(destination)
			
			return

		ctx.voice_state.voice = await destination.connect()
		await ctx.send(f'{config.success} Joined the Voice Channel.')

	@commands.command(description='Summons the bot to a voice channel')
	@commands.has_permissions(manage_guild=True)
	async def summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
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

	@commands.command( aliases=['disconnect'],description="Clear the queue and leave any voice channel")
	@commands.has_permissions(manage_guild=True)
	async def leave(self, ctx: commands.Context):
		"""Clears the queue and leaves the voice channel."""

		cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		for x in collection.find({"_id":ctx.guild.id}):
			dj_roles = x["dj"]

			for roles in dj_roles:
				guild = ctx.guild
								
				role = get(guild.roles, id=roles)
				if role in ctx.author.roles:

					if not ctx.voice_state.voice:
						return await ctx.send(f'{config.forbidden} Not connected to any voice channels.')

					await ctx.voice_state.stop()
					del self.voice_states[ctx.guild.id]
				else:
					await ctx.send(f"{config.forbidden} Only DJs can disconnect the bot.")

	@commands.command(aliases=['current', 'playing'],description='Shows current song')
	async def np(self, ctx: commands.Context):
		"""Displays the currently playing song."""

		await ctx.send(embed=ctx.voice_state.current.create_embed())

	@commands.command(description='Pause the current song')
	async def pause(self, ctx: commands.Context):
		"""Pauses the currently playing song."""

		cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		if ctx.author.guild_permissions.manage_message:
			guild = ctx.guild

			if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
				ctx.voice_state.voice.pause()
				await ctx.message.add_reaction('⏯')
			else:
				await ctx.send(f"{config.forbidden} No music playing.")

		for x in collection.find({"_id":ctx.guild.id}):
			dj_roles = x["dj"]

			for roles in dj_roles:
				guild = ctx.guild
								
				role = get(guild.roles, id=roles)
				if role in ctx.author.roles:
					if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
						ctx.voice_state.voice.pause()
						await ctx.message.add_reaction('⏯')
					else:
						await ctx.send(f"{config.forbidden} No music playing.")

				else:
					await ctx.send(f"{config.forbidden} You're not a DJ to control the music.")

	@commands.command(description='Resume the paused song')
	async def resume(self, ctx: commands.Context):
		"""Resumes a currently paused song."""

		cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		for x in collection.find({"_id":ctx.guild.id}):
			dj_roles = x["dj"]

			for roles in dj_roles:
				guild = ctx.guild
								
				role = get(guild.roles, id=roles)
				if role in ctx.author.roles:
					if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
						ctx.voice_state.voice.resume()
						await ctx.message.add_reaction('⏯')
					else:
						await ctx.send(f"{config.forbidden} Music not paused.")
				else:
					await ctx.send(f"{config.forbidden} You're not a DJ to control the music.")

	@commands.command(description='Stops playing the song and clears the queue')
	async def stop(self, ctx: commands.Context):
		"""Stops playing song and clears the queue."""

		cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		for x in collection.find({"_id":ctx.guild.id}):
			dj_roles = x["dj"]

			for roles in dj_roles:
				guild = ctx.guild
								
				role = get(guild.roles, id=roles)
				if role in ctx.author.roles:

					ctx.voice_state.songs.clear()

					if ctx.voice_state.is_playing:
						ctx.voice_state.voice.stop()
						await ctx.message.add_reaction('⏹')
				else:
					await ctx.send(f"{config.forbidden} You're not a DJ to control the music.")

	@commands.command(description='Vote to skip the song')
	async def skip(self, ctx: commands.Context):
		"""Vote to skip a song. The requester can automatically skip.
		3 skip votes are needed for the song to be skipped.
		"""

		cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
		collection = cluster.DataBase_1.settings

		for x in collection.find({"_id":ctx.guild.id}):
			dj_roles = x["dj"]

			for roles in dj_roles:
				guild = ctx.guild
								
				role = get(guild.roles, id=roles)
				if role in ctx.author.roles:
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

	@commands.command(description='Shows the player queue')
	async def queue(self, ctx: commands.Context, *, page: int = 1):

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

	@commands.command(description='Shuffle the playing song')
	async def shuffle(self, ctx: commands.Context):
		"""Shuffles the queue."""

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send(f'{config.forbidden} The queue is Empty.')

		ctx.voice_state.songs.shuffle()
		await ctx.message.add_reaction(f'{config.success}')

	@commands.command(description='Remove the song from queue')
	async def remove(self, ctx: commands.Context, index: int):
		"""Removes a song from the queue at a given index."""

		if len(ctx.voice_state.songs) == 0:
			return await ctx.send(f'{config.forbidden} The queue is Empty.')

		ctx.voice_state.songs.remove(index - 1)
		await ctx.message.add_reaction(f'{config.success}')

	@commands.command(description='Plays the given song')
	async def play(self, ctx: commands.Context, *, search: str):

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
				await ctx.send(f'{config.forbidden} ' + '{}'.format(str(e)))
			else:
				song = Song(source)

				await ctx.voice_state.songs.put(song)
				await ctx.send(f"{config.success} Song added to queue.")

	@join.before_invoke
	@play.before_invoke
	async def ensure_voice_state(self, ctx: commands.Context):
		if not ctx.author.voice or not ctx.author.voice.channel:
			raise commands.CommandError(f'{config.forbidden} You are currently not connected to any voice channel.')

		if ctx.voice_client:
			if ctx.voice_client.channel != ctx.author.voice.channel:
				raise commands.CommandError(f'{config.forbidden} Already in a voice channel.')


def setup(bot):
	bot.add_cog(Music(bot))
