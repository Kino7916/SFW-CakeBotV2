import logging
from asyncio.tasks import create_task, sleep

from discord.ext import commands

from bot.core.config import settings
from bot.core.server_update import global_cache

STATS_CATEGORY_ID = 1533123743814123612
STATS_CHANNELS: list[dict[str, int | str]] = [
    {
        "channel_id": 1533761873017704451,
        "server_id": 85023,
        "label_name": "Vanilla I"
    },
    {
        "channel_id": 1533761889476149328,
        "server_id": 85024,
        "label_name": "Vanilla U"
    },
    {
        "channel_id": 1533761906958143578,
        "server_id": 85025,
        "label_name": "Yummy"
    }
]
logger = logging.getLogger(__name__)

class StatsUpdater(commands.Cog):
    """Updates statistics channels with servers playercount"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.task = create_task(self.update_interval(5 * 60))


    async def update_stats(self):
        if settings.DEV_GUILD_ID is None:
            return
        
        logger.info("Updating Statistics Channels..")

        for channel_partial in STATS_CHANNELS:
            server = next((s for s in global_cache["servers"] if s["serverId"] == channel_partial["server_id"]), None)
            if server is None:
                logger.warning(f"Missing server cache {channel_partial["label_name"]} ({channel_partial["server_id"]})")
                continue

            guild = self.bot.get_guild(settings.DEV_GUILD_ID) or await self.bot.fetch_guild(settings.DEV_GUILD_ID)
            if guild is None:
                logger.warning("Invalid guild")
                continue
                
            channel = guild.get_channel(int(channel_partial["channel_id"])) or await guild.fetch_channel(int(channel_partial["channel_id"]))
            if channel is None:
                logger.warning(f"Missing channel ({channel_partial["channel_id"]})")
                continue
                
            try:
                str_count = channel.name.split()[-1]
                current_players = str_count.split('/')[0]

                if int(current_players) == server["currentPlayers"]:
                    continue
                await channel.edit(name=f"{channel_partial["label_name"]} {server['currentPlayers']}/{server['maxPlayers']}")
            except Exception as err:
                logger.exception("Exception raised on channel.edit", exc_info=err)
        logger.info("Updating Statistics Channels complete")

    async def update_interval(self, debounce: int):
        while True:
            await sleep(1)
            await self.update_stats()
            await sleep(debounce)

async def setup(bot: commands.Bot):
    await bot.add_cog(StatsUpdater(bot))