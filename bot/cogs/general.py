import logging

import discord
from datetime import datetime
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
    
        
    @app_commands.command(name="interview", description="Use this slash commands to get the interviewer role")
    async def im_back_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = "Yoo cake is back",
            description="IS aliveeee"
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverstats", description="Displays short statistics on playercounts")
    async def serverstats_command(self, interaction: discord.Interaction):
        embed = discord.Embed()
        embed.color = discord.Color.green()
        embed.set_footer(icon_url=interaction.user.display_avatar.url)
        embed.timestamp = datetime.now()
        for server in global_cache["servers"]:
            embed.description = (
                (embed.description or "") + "\n"
                + strip_tags(server["name"]) + "\n"
                + f"Player Count: {server["currentPlayers"]}/{server["maxPlayers"]}" + "\n"
            )
        try:
            await interaction.response.send_message(ephemeral=False, embed=embed)
        except Exception as e:
            logger.error("Something went wrong", exc_info=e)
            
    
async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))