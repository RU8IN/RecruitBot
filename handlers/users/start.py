import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from states.UserStates import CallCenterOp_Test
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(KeyboardButton(text="/test"))
    await message.answer(f'Здравствуйте, {message.from_user.full_name}!\n'
                         f'Это бот RecruitTeamOnline. Здесь вы можете пройти анкетту.', reply_markup=keyboard)
    # await message.answer(f"{message.from_user.id}")
    logging.info([message.from_user.username, message.from_user.id])