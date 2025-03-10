#(¬©)Codexbotz

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL_2, CHANNEL_ID, PORT


ascii_art = """
‚ĖĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚ĖĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚ĖĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēó‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚ĖĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó
‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚ēź‚ēź‚ēĚ‚ēö‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēĒ‚ēĚ‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚Ėą‚Ėą‚ēó‚ēö‚ēź‚ēź‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚ēĚ‚ēö‚ēź‚ēź‚ēź‚ēź‚Ėą‚Ėą‚ēĎ
‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚ēö‚ēź‚ēĚ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚ĖĎ‚ĖĎ‚ĖĎ‚ēö‚Ėą‚Ėą‚Ėą‚ēĒ‚ēĚ‚ĖĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ē¶‚ēĚ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚ĖĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚Ėą‚ēĒ‚ēź‚ēĚ
‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚ēĚ‚ĖĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĒ‚Ėą‚Ėą‚ēó‚ĖĎ‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĒ‚ēź‚ēź‚ēĚ‚ĖĎ‚ĖĎ
‚ēö‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēĒ‚ēĚ‚ēö‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēĒ‚ēĚ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēĒ‚ēĚ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚ēĒ‚ēĚ‚ēö‚Ėą‚Ėą‚ēó‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ē¶‚ēĚ‚ēö‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēĒ‚ēĚ‚ĖĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚ēĎ‚ĖĎ‚ĖĎ‚ĖĎ‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚Ėą‚ēó
‚ĖĎ‚ēö‚ēź‚ēź‚ēź‚ēź‚ēĚ‚ĖĎ‚ĖĎ‚ēö‚ēź‚ēź‚ēź‚ēź‚ēĚ‚ĖĎ‚ēö‚ēź‚ēź‚ēź‚ēź‚ēź‚ēĚ‚ĖĎ‚ēö‚ēź‚ēź‚ēź‚ēź‚ēź‚ēź‚ēĚ‚ēö‚ēź‚ēĚ‚ĖĎ‚ĖĎ‚ēö‚ēź‚ēĚ‚ēö‚ēź‚ēź‚ēź‚ēź‚ēź‚ēĚ‚ĖĎ‚ĖĎ‚ēö‚ēź‚ēź‚ēź‚ēź‚ēĚ‚ĖĎ‚ĖĎ‚ĖĎ‚ĖĎ‚ēö‚ēź‚ēĚ‚ĖĎ‚ĖĎ‚ĖĎ‚ēö‚ēź‚ēź‚ēź‚ēź‚ēź‚ēź‚ēĚ
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Fetch invite link for the first force-sub channel
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit()

        # Fetch invite link for the second force-sub channel
        if FORCE_SUB_CHANNEL_2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Second Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL_2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL_2}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit()

        # Check DB channel
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/CodeXBotz")
        print(ascii_art)
        print("""Welcome to CodeXBotz File Sharing Bot""")
        self.username = usr_bot_me.username
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
