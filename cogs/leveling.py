from numix_imports import *

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")
        print('"Leveling" cog loaded')


    @commands.Cog.listener()
    async def on_message(self, message):
        return
        mongo_url = "mongodb+srv://Benitz:6vsdPiReMc2nTukr@numix.dksdu.mongodb.net/<dbname>?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["DataBase_1"]
        collection = db["Leveling"]
        author_id = message.author.id
        guild_id = message.guild.id

        user_id = {"_id": author_id}

        if message.author.bot:
            return

        if(collection.count_documents({}) == 0):
            user_info = {"_id": author_id, "GuildID": guild_id, "Level": 1, "XP": 0}
            collection.insert_one(user_info)

        await message.channel.send("User added to DataBase.")

def setup(bot):
    bot.add_cog(Leveling(bot))