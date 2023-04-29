from aiohttp import ClientSession
from .meta import SingletonMeta
import asyncio
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

bot_api_key = os.environ.get("BOT_API_KEY")
chat_id_to_send = os.environ.get("CHAT_ID")


class NetworkManager(metaclass=SingletonMeta):
    # __params = {}
    async def send_create(self, message):
        url = "https://api.telegram.org/bot" + bot_api_key + "/sendMessage?chat_id=" + chat_id_to_send + "&text="+message
        async with ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                    # await asyncio.sleep(0.01)
                    # data = json.loads(self.__data)
                    # await db.DataBaseManager().update_all_data(data)
                else:
                    logging.info("Request error")
                    await asyncio.sleep(0.01)

    async def fetch_tinkoff_data(self, item):
        async with ClientSession() as session:
            async with session.get(item[1]) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    logging.info(item)
                    logging.info("Request error")
                    await asyncio.sleep(0.01)
