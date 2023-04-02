from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.config_helper import DotEnvHelper

import treasure_handle

env: DotEnvHelper  = DotEnvHelper()
storage: MemoryStorage = MemoryStorage()

api_key = env.get_value('MAPS_API_KEY')
treasure_handle.api_key = api_key

bot: Bot = Bot(env.get_value(env.BOT_TOKEN_FIELD), parse_mode='MarkdownV2')
treasure_handle.bot = bot
dp: Dispatcher = Dispatcher(bot, storage=storage)

dp.register_message_handler(treasure_handle.treasure_handle, content_types=types.ContentTypes.PHOTO)

# Handler for all other messages
# dp.register_message_handler(error_handle)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)