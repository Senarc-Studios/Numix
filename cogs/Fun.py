from numix_imports import *

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.alex_api_token = self.config.alexflipnote_api
		print('"Fun" cog loaded')

	async def randomimageapi(self, ctx, url: str, endpoint: str, token: str = None):
		try:
			r = await http.get(url, res_method="json", no_cache=True, headers={"Authorization": token})
		except aiohttp.ClientConnectorError:
			return await ctx.send(":no_entry_sign: The API is currently down, Try again later.")
		except aiohttp.ContentTypeError:
			return await ctx.send(":fire: API returned an error.")

		await ctx.send(r[endpoint])

	async def api_img_creator(self, ctx, url: str, filename: str, content: str = None, token: str = None):
		async with ctx.channel.typing():
			req = await http.get(url, res_method="read", headers={"Authorization": token})

			if not req:
				return await ctx.send(":fire: Error while creating an image.")

			bio = BytesIO(req)
			bio.seek(0)
			await ctx.send(content=content, file=discord.File(bio, filename=filename))
	
	@commands.command(name="8ball")
	async def _8ball(self, ctx, *, input):
		responces = ["It is certain", "Without a doubt", "You may rely on it", "Yes definitely", "It is decidedly so", "As I see it, yes", "Most likely", "Yes", "Outlook good", "Signs point to yes", "Reply hazy try again", "Better not tell you now", "Ask again later", "Cannot predict now", "Concentrate and ask again", "Don’t count on it", "Outlook not so good", "My sources say no", "Very doubtful", "My reply is no"]
		embed = discord.Embed(timestamp=ctx.message.created_at, title="8Ball", description=f"**Question:** {input}\n\n**Answer:** {choice(responces)}", color=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
	async def cat(self, ctx):
		""" Posts a random cat """
		await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/cats', 'file', token=self.alex_api_token)

	@commands.command()
	@commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
	async def dog(self, ctx):
		""" Posts a random dog """
		await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/dogs', 'file', token=self.alex_api_token)

	@commands.command(aliases=["bird"])
	@commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
	async def bird(self, ctx):
		""" Posts a random birb """
		await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/birb', 'file', token=self.alex_api_token)

	@commands.command()
	@commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
	async def duck(self, ctx):
		""" Posts a random duck """
		await self.randomimageapi(ctx, 'https://random-d.uk/api/v1/random', 'url')

	@commands.command()
	@commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
	async def coffee(self, ctx):
		""" Posts a random coffee """
		await self.randomimageapi(ctx, 'https://coffee.alexflipnote.dev/random.json', 'file')

	@commands.command(aliases=['flip', 'coin'])
	async def coinflip(self, ctx):
		""" Coinflip! """
		coinsides = ['Heads', 'Tails']
		embed = discord.Embed(timestamp=ctx.message.created_at, title="Coinflip", description=f"\nflipped a coin and got **{random.choice(coinsides)}**!", color=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command()
	async def supreme(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True)):
		parser = argparser.Arguments()
		parser.add_argument('input', nargs="+", default=None)
		parser.add_argument('-d', '--dark', action='store_true')
		parser.add_argument('-l', '--light', action='store_true')

		args, valid_check = parser.parse_args(text)
		if not valid_check:
			return await ctx.send(args)

		inputText = urllib.parse.quote(' '.join(args.input))
		if len(inputText) > 500:
			return await ctx.send(f"**{ctx.author.name}**, the Supreme API is limited to 500 characters, sorry.")

		darkorlight = ""
		if args.dark:
			darkorlight = "dark=true"
		if args.light:
			darkorlight = "light=true"
		if args.dark and args.light:
			return await ctx.send(f"**{ctx.author.name}**, you can't define both --dark and --light, sorry..")

		await self.api_img_creator(ctx, f"https://api.alexflipnote.dev/supreme?text={inputText}&{darkorlight}", "supreme.png", token=self.alex_api_token)

	@commands.command(aliases=["dict", "dictionary", "meaning"])
	@commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
	async def urban(self, ctx, *, search: commands.clean_content):
		""" Find the 'best' definition to your words """
		try:
			url = await http.get(f'https://api.urbandictionary.com/v0/define?term={search}', res_method="json")
		except Exception:
			return await ctx.send(":no_entry_sign: Urban API returned invalid data.")
		if not url:
			return await ctx.send(":fire: an Error has occured.")

		if not len(url['list']):
			return await ctx.send(":no_entry_sign: Couldn't find your search in the dictionary.")
		result = sorted(url['list'], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]
		definition = result['definition']
		if len(definition) >= 1000:
			definition = definition[:1000]
			definition = definition.rsplit(' ', 1)[0]
			definition += '...'
		embed = discord.Embed(timestamp=ctx.message.created_at, title="Urban Dictionary", description=f"**Search:** {search}\n\n**Result:** {result['word']}\n```fix\n{definition}```", color=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command()
	async def rate(self, ctx, *, thing: commands.clean_content):
		rate_amount = random.uniform(0.0, 100.0)
		embed = discord.Embed(timestamp=ctx.message.created_at, title="Random Rate", description=f"Rating for `{thing}` is **{round(rate_amount, 4)} / 100**")
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command(aliases=['noticemesenpai'])
	async def noticeme(self, ctx):
		if not permissions.can_handle(ctx, "attach_files"):
			return await ctx.send(":no_entry_sign: No image perms")

		bio = BytesIO(await http.get("https://i.alexflipnote.dev/500ce4.gif", res_method="read"))
		await ctx.send(file=discord.File(bio, filename="noticeme.gif"))

	@commands.command(aliases=['slots', 'bet'])
	@commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
	async def slot(self, ctx):
		""" Roll the slot machine """
		emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
		a = random.choice(emojis)
		b = random.choice(emojis)
		c = random.choice(emojis)

		slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

		if (a == b == c):
			embed = discord.Embed(timestamp=ctx.message.created_at, title="Slot Machine", description=f"\n{slotmachine}\n\nAll matching, you won! :confetti_ball:", color=242424)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)
		elif (a == b) or (a == c) or (b == c):
			embed = discord.Embed(timestamp=ctx.message.created_at, title="Slot Machine", description=f"\n{slotmachine}\n\n2 in a row, you won! 🎉", color=242424)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(timestamp=ctx.message.created_at, title="Slot Machine", description=f"\n{slotmachine}\n\nNo match, you lost :money_with_wings:", color=242424)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Fun(bot))