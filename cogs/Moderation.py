from numix_imports import *


def blacklist_check():
    def predicate(ctx):
        author_id = ctx.author.id
        if blacklist_admin.find_one({'user_id': author_id}):
            return False
        return True
    return commands.check(predicate)


class Moderation(commands.Cog, name='Moderation'):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command()
    @blacklist_check()
    async def ping(self, ctx):
        time = int(self.bot.latency * 1000)
        await ctx.send(
            embed=create_embed(
                f'The ping is {time} ms!'
            ),
            delete_after=10
        )

def setup(bot):
    bot.add_cog(Moderation(bot))
