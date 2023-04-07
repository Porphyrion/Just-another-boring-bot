from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.config_helper import DotEnvHelper

import treasure_handle

env: DotEnvHelper  = DotEnvHelper()
storage: MemoryStorage = MemoryStorage()


bot: Bot = Bot(env.get_value(env.BOT_TOKEN_FIELD))
dp: Dispatcher = Dispatcher(bot, storage=storage)
treasure_handle.bot = bot


dp.register_message_handler(treasure_handle.treasure_handle, content_types=types.ContentTypes.PHOTO)
dp.register_message_handler(treasure_handle.treasure_rejecte)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)