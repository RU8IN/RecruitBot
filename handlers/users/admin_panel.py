from loader import dp

from data.config import admins
from aiogram import types


@dp.message_handler(commands=["hello"], user_id=admins, state="*")
async def hello_world(message: types.Message):
    await message.reply("Hello World!")