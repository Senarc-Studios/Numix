from numix_imports import *

class Guild_Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")
        self.MONGO = self.config.db1
        self.MONGO_CONNECTION = MongoClient(self.MONGO)
        self.db = self.MONGO_CONNECTION.DataBase_1.settings
        print("\"Guild_Events\" cog loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        MONGO_GUILD_SETTINGS = self.db.find_one({ "_id": member.guild.id })
        channel = discord.utils.get(member.guild.TextChannels, id=MONGO_GUILD_SETTINGS["jm"])
        MEMBER_COUNT_RAW = f"{len(member.guild.users)}"
        if MEMBER_COUNT_RAW.endswith("1"):
            MEMBER_COUNT = f"{MEMBER_COUNT_RAW}st Member"

        elif MEMBER_COUNT_RAW.endswith("2"):
            MEMBER_COUNT = f"{MEMBER_COUNT_RAW}nd Member"

        elif MEMBER_COUNT_RAW.endswith("3"):
            MEMBER_COUNT = f"{MEMBER_COUNT_RAW}rd Member"

        else:
            MEMBER_COUNT = f"{MEMBER_COUNT_RAW}th Member"

        embed = discord.Embed(color=242424, description=f"Looks like someone new joined, Welcome {member.name}! We hope you have a nice stay! Make sure you read the rules.")
        embed.set_author(name=f"{member.name}", icon_url=member.avatar_url)
        embed.set_image(url="https://media.giphy.com/media/8PyTvI5EOu9LbAm8uS/giphy.gif")
        embed.set_footer(f"{MEMBER_COUNT}", icon_url=member.guild.icon_url)
        channel.send(embed=embed)