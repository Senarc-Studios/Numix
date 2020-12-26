from numix_imports import *

class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")
        print('"Tests" cog loaded')

    @commands.command()
    @commands.is_owner()
    async def dbtest(self, ctx):
        
        client = pymongo.MongoClient("mongodb+srv://Benitz:6vsdPiReMc2nTukr@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority")
        db = client.test

        test = {"command":1}
        db.insert_one(test)

        await ctx.send("**DB Test Successful.**")

def setup(bot):
    bot.add_cog(Tests(bot))