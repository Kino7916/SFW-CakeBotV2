from discord.ext import commands


class Deprecated(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="server")
    async def servers_command(self, ctx: commands.Context):
        await ctx.reply("https://static2.klipy.com/ii/a8ada81afc59159ea5c8927feffa2e31/fe/3e/km0AUNJRv5AxqtIkWos.gif")
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Deprecated(bot))