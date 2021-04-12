from numix_imports import *
import numix_encrypt

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")
		self.alex_api_token = self.config.alexflipnote_api
		self.discordrep_api = self.config.discordrep_api_token
		print('"Fun" cog loaded')

	async def developers(ctx):
		devs = [529499034495483926, 727365670395838626, 526711399137673232]
		if ctx.author.id in devs:
			return True

		else:
			await ctx.send(f"{self.config.forbidden} You can't use that command.")
			return False

	async def date_now(ctx):
		date_1 = f"{ctx.message.created_at.__format__('%d-%B-%Y @ %H:%M:%S')}"
		date_2 = date_1.replace("January", "01")
		date_3 = date_2.replace("February", "02")
		date_4 = date_3.replace("March", "03")
		date_5 = date_4.replace("April", "04")
		date_6 = date_5.replace("May", "05")
		date_7 = date_6.replace("June", "06")
		date_8 = date_7.replace("July", "07")
		date_9 = date_8.replace("August", "08")
		date_10 = date_9.replace("September", "09")
		date_11 = date_10.replace("October", "10")
		date_12 = date_11.replace("November", "11")
		date_13 = date_12.replace("December", "12")
		Today = date_13
		return Today

	async def rep(self, ctx, url: str, endpoint: str):
		try:
			r = await http.get(url, res_method="json", no_cache=True, headers={"Authorization": self.discordrep_api})
		except aiohttp.ClientConnectorError:
			return await ctx.send(f"{self.config.forbidden} The API is currently down, Try again later.")
		except aiohttp.ContentTypeError:
			return await ctx.send(":fire: API returned an error.")

		await ctx.send(r[endpoint])

	async def randomimageapi(self, ctx, url: str, endpoint: str, token: str = None):
		try:
			r = await http.get(url, res_method="json", no_cache=True, headers={"Authorization": token})
		except aiohttp.ClientConnectorError:
			return await ctx.send(f"{self.config.forbidden} The API is currently down, Try again later.")
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

	@commands.command(aliases=["who-crypt", "who-nucrypt", "whos-key"])
	@commands.check(developers)
	async def whocrypt(self, ctx, key):
		if key is None:
			await ctx.send(f"{self.config.forbidden} Provide a Key to decrypt text.")

		else:
			cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
			collection = cluster.DataBase_1.nucrypt
			await ctx.message.delete()
			for key in collection.find({ "_id": f"{key}" }):
				text = key['decrypted']
				author_discord = key['whocrypt_author']
				server_discord = key['whocrypt_server']
				date = key['Date']
				time = key['Time']

				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"**Decrypted Text:**\n{text}\n\n**Author:**\n{author_discord}\n\n**Server:**\n{server_discord}\n\n**Date:**\n{date}\n\n**Time:**\n{time}", color=242424)
				embed.set_author(name="Whocrypt Information", icon_url=ctx.author.avatar_url)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await ctx.send(embed=embed)
				if text is None:
					await ctx.send(f"{self.config.forbidden} That key doesn't exist.")

	@commands.command(aliases=["numix-encrypt", "encrypt"])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def nucrypt(self, ctx, *, body=None):
		date_1 = f"{ctx.message.created_at.__format__('%d-%B-%Y')}"
		date_2 = date_1.replace("January", "01")
		date_3 = date_2.replace("February", "02")
		date_4 = date_3.replace("March", "03")
		date_5 = date_4.replace("April", "04")
		date_6 = date_5.replace("May", "05")
		date_7 = date_6.replace("June", "06")
		date_8 = date_7.replace("July", "07")
		date_9 = date_8.replace("August", "08")
		date_10 = date_9.replace("September", "09")
		date_11 = date_10.replace("October", "10")
		date_12 = date_11.replace("November", "11")
		date_13 = date_12.replace("December", "12")
		Today = date_13

		if body is None:
			await ctx.send(f"{self.config.forbidden} Provide some text that you want to be encrypted.")
		
		else:
			await ctx.message.delete()
			if ctx.message.content.endswith("--s"):
				if ctx.author.id == ctx.guild.owner_id:

					Author = ctx.author
					text = body.replace("--s", "")
					cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
					collection = cluster.DataBase_1.nucrypt

					key = numix_encrypt.encrypt()
					key_in_plain_text = f"{key}"

					collection.insert_one({ "_id": f"{key_in_plain_text}", "decrypted": f"{text}", "author": f"*Anonymous*", "server": f"*Anonymous*", "whocrypt_author": f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", "whocrypt_server": f"{ctx.guild.name}(`{ctx.guild.id}`)", "Date": str(Today), "Time": ctx.message.created_at.__format__('%H:%M:%S') })

					embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You can **Nu-Decrypt** to get the plain text.\n**Key:** `{key_in_plain_text}`", color=242424)
					embed.set_author(name=f"Anonymously Encrypted", icon_url=ctx.author.avatar_url)
					embed.set_footer(text="Numix", icon_url=self.config.logo)
					await Author.send(embed=embed)
					await ctx.send(f"{self.config.success} Encrypted Text and Sent Key in DMs.")

				else:
					await ctx.send(f"{self.config.forbidden} Only server owners can do `--s`.")

			elif ctx.message.content.endswith("-s"):
				if ctx.author.guild_permissions.administrator:

					text = body.replace("-s", "")
					Author = ctx.author
					cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
					collection = cluster.DataBase_1.nucrypt

					key = numix_encrypt.encrypt()
					key_in_plain_text = f"{key}"

					collection.insert_one({ "_id": f"{key_in_plain_text}", "decrypted": f"{text}", "author": f"*Anonymous*", "server": f"*Anonymous*", "whocrypt_author": f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", "whocrypt_server": f"{ctx.guild.name}(`{ctx.guild.id}`)", "Date": str(Today), "Time": ctx.message.created_at.__format__('%H:%M:%S') })

					embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You can **Nu-Decrypt** to get the plain text.\n**Key:** `{key_in_plain_text}`", color=242424)
					embed.set_author(name=f"Anonymously Encrypted", icon_url=ctx.author.avatar_url)
					embed.set_footer(text="Numix", icon_url=self.config.logo)
					await Author.send(embed=embed)
					await ctx.send(f"{self.config.success} Encrypted Text and Sent Key in DMs.")

				else:
					await ctx.send(f"{self.config.forbidden} Only server administrators can do `-s`.")

			else:
				text = body
				Author = ctx.author
				cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
				collection = cluster.DataBase_1.nucrypt

				key = numix_encrypt.encrypt()
				key_in_plain_text = f"{key}"

				collection.insert_one({ "_id": f"{key_in_plain_text}", "decrypted": f"{text}", "author": f"*Anonymous*", "server": f"*Anonymous*", "whocrypt_author": f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", "whocrypt_server": f"{ctx.guild.name}(`{ctx.guild.id}`)", "Date": str(Today), "Time": ctx.message.created_at.__format__('%H:%M:%S') })

				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"You can **Nu-Decrypt** to get the plain text.\n**Key:** `{key_in_plain_text}`", color=242424)
				embed.set_author(name=f"Encrypted", icon_url=ctx.author.avatar_url)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await Author.send(embed=embed)
				await ctx.send(f"{self.config.success} Encrypted Text and Sent Key in DMs.")

	@commands.command(aliases=["Nu-Decrypt", "nu-decrypt", "decrypt"])
	async def nudecrypt(self, ctx, *, key=None):
		Author = ctx.author
		if key is None:
			await ctx.send(f"{self.config.forbidden} Provide a Key to decrypt text.")

		else:
			cluster = MongoClient('mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority')
			collection = cluster.DataBase_1.nucrypt
			await ctx.message.delete()
			for key in collection.find({ "_id": f"{key}" }):
				text = key['decrypted']
				author_discord = key['author']
				server_discord = key['server']

				embed = discord.Embed(timestamp=ctx.message.created_at, description=f"**Decrypted Text:**\n{text}\n\n**Author:**\n{author_discord}\n\n**Server:**\n{server_discord}", color=242424)
				embed.set_author(name="Decrypted", icon_url=ctx.author.avatar_url)
				embed.set_footer(text="Numix", icon_url=self.config.logo)
				await Author.send(embed=embed)
				await ctx.send(f"{self.config.success} Your key has been decrypted and sent in DMs.")
				if text == "":
					await ctx.send(f"{self.config.forbidden} That key doesn't exist.")

	@commands.command(aliases=["dice", "dise"])
	async def roll(self, ctx):
		dice = ["1", "2", "3", "4", "5", "6"]
		embed = discord.Embed(timestamp=ctx.message.created_at, description=f"Dice has been rolled. The number is **{random.choice(dice)}**.", color=242424)
		embed.set_author(name="Rolled a Dice", icon_url=ctx.author.avatar_url)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

	@commands.command(name="8ball")
	async def _8ball(self, ctx, *, input=None):
		if input is None:
			return await ctx.send(f"{self.config.forbidden} Specify what you need to be predicted.")

		responces = ["It is certain", "Without a doubt", "You may rely on it", "Yes definitely", "It is decidedly so", "As I see it, yes", "Most likely", "Yes", "Outlook good", "Signs point to yes", "Reply hazy try again", "Better not tell you now", "Ask again later", "Cannot predict now", "Concentrate and ask again", "Don’t count on it", "Outlook not so good", "My sources say no", "Very doubtful", "My reply is no"]
		embed = discord.Embed(timestamp=ctx.message.created_at, title="8Ball", description=f"**Question:** {input}\n\n**Answer:** {choice(responces)}", color=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)


	@commands.command(aliases=["dict", "dictionary", "meaning"])
	@commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
	async def urban(self, ctx, *, search: commands.clean_content=None):
		
		if not ctx.channel.is_nsfw():
			return await ctx.send(f"{self.config.forbidden} This command can only be used in a NSFW channel.")

		if search is None:
			return await ctx.send(f"{self.config.forbidden} Specify what you need to be searched in the urban dictionary.")

		""" Find the 'best' definition to your words """
		try:
			url = await http.get(f'https://api.urbandictionary.com/v0/define?term={search}', res_method="json")
		except Exception:
			return await ctx.send(f"{self.config.forbidden} Urban API returned invalid data.")
		if not url:
			return await ctx.send(":fire: an Error has occured.")

		if not len(url['list']):
			return await ctx.send(f"{self.config.forbidden} Couldn't find your search in the dictionary.")
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
	async def rate(self, ctx, *, thing: commands.clean_content=None):
		if thing is None:
			return await ctx.send(f"{self.config.forbidden} Specify what you want me to rate on.")
		rate_amount = random.uniform(0.0, 100.0)
		embed = discord.Embed(timestamp=ctx.message.created_at, title="Random Rate", description=f"Rating for `{thing}` is **{round(rate_amount, 4)} / 100**", color=242424)
		embed.set_footer(text="Numix", icon_url=self.config.logo)
		await ctx.send(embed=embed)

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