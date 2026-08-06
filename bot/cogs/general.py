import logging

import discord
from discord import app_commands
from discord.ext import commands
from strip_tags import strip_tags

from ..core.server_update import global_cache

logger = logging.getLogger(__name__)


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="info", description="Info about the bot")
    async def im_back_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = "CakeBot v2 info",
            description="CakeBot player list updates every 5 minutes.\nTo check the player list, see the channels under the statistics category.\nUser /help to see the bot comamnds",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="server", description="Get Server player info")
    async def server_command(self, interaction: discord.Interaction):
        descriptionText = ""
        embed = discord.Embed(
            description=descriptionText,
            url="https://static2.klipy.com/ii/a8ada81afc59159ea5c8927feffa2e31/fe/3e/km0AUNJRv5AxqtIkWos.gif",
            type="gifv"
        )
        for server in global_cache["servers"]:
            embed.description = str(embed.description) + f"\n"
        await interaction.response.send_message(ephemeral=True, embed=embed)
        
    @app_commands.command(name="interview", description="Use this slash commands to get the interviewer role")
    async def im_back_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = "Yoo cake is back",
            description="IS aliveeee"
        )
        await interaction.response.send_message(embed=embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))