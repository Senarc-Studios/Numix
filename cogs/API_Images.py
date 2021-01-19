from numix_imports import * 
import requests

class API_Images(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.config = default.get("./config.json")

	@commands.command(description="Sends a random cat image")
	async def cat(self, ctx):
		URL = f'https://api.thecatapi.com/v1/images/search'

		def check_valid_status_code(request):
			if request.status_code == 200:
				return request.json()

			return False

		def get_cat():
			request = requests.get(URL)
			data = check_valid_status_code(request)

			return data

		cat = get_cat()
		if not cat:
			await ctx.channel.send(
				"Couldn't get cat from API. Try again later.")

		else:
			#print(cat)
			cat = cat[0]['url']
			#agee = str(cat['url'])
			embed = discord.Embed(timestamp=ctx.message.created_at, color=242424)
			embed.set_author(name="Cat", icon_url=ctx.author.avatar_url)
			embed.set_footer(text="Numix", icon_url=self.config.logo)
			embed.set_image(url=f"{cat}")
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(API_Images(bot))
