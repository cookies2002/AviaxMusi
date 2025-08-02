import sys
if sys.platform != "win32":
    import uvloop
    uvloop.install()

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
from ..logging import LOGGER


class Aviax(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="AviaxMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        # 🧪 Debug to check log group ID
        try:
            log_group_id = config.LOG_GROUP_ID
            assert isinstance(log_group_id, int)
        except Exception:
            LOGGER(__name__).error("❌ LOG_GROUP_ID must be an integer. Check your .env or config.")
            exit()

        # ✅ Try sending a test log message
        try:
            await self.send_message(
                chat_id=log_group_id,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username or 'N/A'}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("❌ Bot failed to access the log group. Make sure the bot is added and the group ID is correct.")
            exit()
        except Exception as ex:
            LOGGER(__name__).error(f"❌ Could not send log message. Reason: {type(ex).__name__}: {ex}")
            exit()

        # ✅ Check if bot is an admin in log group
        try:
            chat_member = await self.get_chat_member(log_group_id, self.id)
            if chat_member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("❌ Please promote your bot as an admin in the log group.")
                exit()
        except Exception as ex:
            LOGGER(__name__).error(f"❌ Failed to check bot admin status. Reason: {type(ex).__name__}: {ex}")
            exit()

        LOGGER(__name__).info(f"✅ Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
