from numix_imports import *

client = pymongo.MongoClient(os.environ.get('dbconn'))
db = client['DaedBot']
guildcol = db['prefix']
queuecol = db['queue']
playlistcol = db['playlist']
blacklist_admin = db['adminblacklist']


def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklist_admin.find_one({'user_id': author_id}):
            return False
        return True
    return commands.check(predicate)


class Moderation(commands.Cog, name='Moderation'):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(
        name='ping',
        description='Check the latency',
        usage='`.ping`'
    )
    @blacklist_check()
    async def ping(self, ctx):
        time = int(self.client.latency * 1000)
        await ctx.send(
            embed=create_embed(
                f'The ping is {time} ms!'
            ),
            delete_after=10
        )

def setup(client):
    client.add_cog(Moderation(client))
