from numix_imports import *

mongo_url = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"
cluster = MongoClient(mongo_url)
level = cluster["DataBase_1"]['Leveling']

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")
        print('"Leveling" cog loaded')


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        elif message.guild is None:
            return 

        # Checks for dm and bot 

        stats = level.find_one({'_id' : message.author.id})
        try:
            if stats is None:
                newuser = {"_id": message.author.id,"GuildID" : message.guild.id,"Level" : 1,"XP": 0}
                level.insert_one(newuser)

            else:
                current_xp = stats['XP']
                print(current_xp)
                new_xp = current_xp + 5
                print(new_xp)
                level.update_one({"_id": message.author.id}, {"$set": {"XP": new_xp}})

                lvl_start = stats['Level']
                if stats['XP'] >= round(lvl_start * 2 * 100):
                    new_lvl  = lvl_start + 1
                    level.update_one({"_id": message.author.id}, {"$set": {"Level": new_lvl}})
                    await message.channel.send(f":tada: {message.author.mention} You leveled up to **Level {new_level}** :tada:")


                

        except Exception:
            pass

        """
        # Beni code ( Backup )
        author_id = message.author.id
        guild_id = message.guild.id
        user_id = {"_id": author_id, "GuildID": guild_id}

        if message.author.bot:
            return

        if level.count_documents({ "_id": author_id, "GuildID": guild_id }) == 0:
            user_info = {"_id": author_id, "GuildID": guild_id, "Level": 1, "XP": 0}
            level.insert_one(user_info)

        exp = collection.find(user_id)
        for xp in exp:
            cur_xp = xp['XP']

            new_xp = cur_xp + 5

            level.update_one({ "_id": author_id }, { "$set": { "XP":new_xp } }, upsert=True)

            lvl_start = xp['Level']

            new_level = lvl_start + 1

            if cur_xp >= round(lvl_start * 2 * 100):

                level.update_one({ "_id": author_id, "GuildID": guild_id }, { "$set": { "Level": new_level } }, upsert=True)
                await message.channel.send(f":tada: {message.author.mention} You leveled up to **Level {new_level}** :tada:")

        """

def setup(bot):
    bot.add_cog(Leveling(bot))