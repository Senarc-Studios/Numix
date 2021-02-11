from numix_imports import *
import motor.motor_asyncio

mongo_url = "mongodb+srv://Benitz:4mWMn7ety6HrIRIx@numix.dksdu.mongodb.net/DataBase_1?retryWrites=true&w=majority"
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
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

        stats = await level.find_one({'_id' : message.author.id})
        try:
            if stats is None:
                newuser = {"_id": message.author.id, "GuildID": message.guild.id,"Level" : 1,"XP": 0}
                await level.insert_one(newuser)

            else:
                current_xp = stats['XP']
                new_xp = current_xp + 5
                await level.update_one({"_id": message.author.id}, {"$set": {"XP": new_xp}})

                lvl_start = stats['Level']
                if stats['XP'] >= round(lvl_start * 2 * 100):
                    new_lvl  = lvl_start + 1
                    await level.update_one({"_id": message.author.id}, {"$set": {"Level": new_lvl}})
                    await message.channel.send(f":tada: {message.author.mention} You leveled up to **Level {new_lvl}** :tada:")

        except Exception:
            pass

def setup(bot):
    bot.add_cog(Leveling(bot))