import logging
from asyncio.tasks import create_task, sleep

import datetime
import discord
from discord.ext import commands

from bot.constants import STATS_CATEGORY_ID, STATS_CHANNEL_ID, STATS_SERVERS
from bot.core.config import settings
from bot.core.server_update import global_cache

STATS_MESSAGE_ID = 0


logger = logging.getLogger(__name__)
is_updating = False
stats_embed = discord.Embed(colour=discord.Colour.from_str("#ff0059"))
stats_embed.set_author(name="Server Statistics", icon_url="https://limbuscompany.wiki.gg/images/thumb/MD7_Projection_Rate.png/179px-MD7_Projection_Rate.png?b79433")
stats_embed.set_thumbnail(url="https://limbuscompany.wiki.gg/images/thumb/MD6_Projection_Rate.png/176px-MD6_Projection_Rate.png?250898")
stats_embed.set_image(url="https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/700330/57931a3aa75ae823086fd945d891d6a5c98d6172/header.jpg?t=1792263389")
stats_embed.description = "You can view our server stats right here!"
stats_embed.set_footer(text="Retrieved from scplist.kr")

try:
    with open("stat_channel.txt", "rt") as f:
        if f.readable():
            msg_id = f.read()
            logger.info(f"str={msg_id}\nint={int(msg_id)}")
            if msg_id is not None:
                STATS_MESSAGE_ID = int(msg_id)
except:
    pass

class StatsUpdater(commands.Cog):
    """Updates statistics channels with servers playercount"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.task = create_task(self.update_stats_interval(15))
        self.task2 = create_task(self.update_old_stats_interval(5 * 60))

    async def update_stats(self):
        global STATS_MESSAGE_ID
        if settings.DEV_GUILD_ID is None:
            return

        guild = self.bot.get_guild(settings.DEV_GUILD_ID) or await self.bot.fetch_guild(settings.DEV_GUILD_ID)
        if guild is None:
            logger.warning("Guild is missing")
            return
        stats_embed.set_thumbnail(url=guild.icon.url)

        stat_channel = guild.get_channel(STATS_CHANNEL_ID) or await guild.fetch_channel(STATS_CHANNEL_ID)
        if stat_channel is None:
            logger.warning("No channel is found")
            return

        message = None
        try:
            message = await stat_channel.fetch_message(STATS_MESSAGE_ID) if STATS_MESSAGE_ID != 0 else None
        except Exception as e:
            logger.error(e)
            pass

        self.update_embed()
        
        if message is None:
            message = await stat_channel.send(embed=stats_embed)

            STATS_MESSAGE_ID = message.id
            with open("stat_channel.txt", "wt") as f:
                f.write(str(message.id))
        else:
            await message.edit(embed=stats_embed)

    def update_embed(self):
        global is_updating
        is_updating = True
        stats_embed.clear_fields()
        stats_embed.timestamp = datetime.datetime.now()
        for server_info in STATS_SERVERS:
            stat_info = next((s for s in global_cache["servers"] if s["serverId"] == server_info["server_id"]), None)
            status_text = "<:sv_offline:1566495728635871312> Offline - N/A"
            if stat_info is None:
                logger.warning(f"Missing server cache {server_info["label_name"]} ({server_info["server_id"]})")
            else:
                status_text = f"<:sv_online:1566495562830708766> Online - {stat_info["currentPlayers"]}/{stat_info["maxPlayers"]}"
            stats_embed.add_field(name=f"Eagle's {server_info["label_name"]}", value=status_text, inline=False)

        is_updating = False

    async def update_old_stats(self):
        if settings.DEV_GUILD_ID is None:
            return
        
        logger.info("Updating Statistics Channels..")
        
        for server_info in STATS_SERVERS:
            
            try:
                stat_info = next((s for s in global_cache["servers"] if s["serverId"] == server_info["server_id"]), None)
                if stat_info is None:
                    logger.warning(f"Missing server cache {server_info["label_name"]} ({server_info["server_id"]})")
                    continue

                guild = self.bot.get_guild(settings.DEV_GUILD_ID) or await self.bot.fetch_guild(settings.DEV_GUILD_ID)
                if guild is None:
                    logger.warning("Invalid guild")
                    continue

                channel = guild.get_channel(int(server_info["channel_id"])) or await guild.fetch_channel(int(server_info["channel_id"]))
                if channel is None:
                    logger.warning(f"Missing channel ({server_info["channel_id"]})")
                    continue
                
                str_count = channel.name.split()[-1]
                current_players = str_count.split('/')[0]

                name = f"{server_info["label_name"]} {stat_info['currentPlayers']}/{stat_info['maxPlayers']}"
                if int(current_players) == stat_info["currentPlayers"]:
                    if channel.name == name:
                        continue
                
                await channel.edit(name=name)
            except Exception as err:
                logger.exception("Exception raised on channel.edit", exc_info=err)
        logger.info("Updating Statistics Channels complete")

    async def update_stats_interval(self, debounce: int):
        while True:
            await sleep(1)
            await self.update_stats()
            await sleep(debounce)

    async def update_old_stats_interval(self, debounce: int):
        while True:
            await sleep(5)
            await self.update_old_stats()
            await sleep(debounce)

async def setup(bot: commands.Bot):
    await bot.add_cog(StatsUpdater(bot))