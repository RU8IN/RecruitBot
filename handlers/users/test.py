import logging
import time

from aiogram.dispatcher.filters.filters import BoundFilter

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data.config import admins
from loader import dp, bot
from states.UserStates import CallCenterOp_Test


@dp.message_handler(commands="test", state="*")
async def test_handler_1(message: types.Message, state: FSMContext):
    await message.answer("Вы всегда можете отменить тест, написав /cancel_test")
    time.sleep(1)
    await message.answer("Ваше имя?", reply_markup=types.ReplyKeyboardRemove())
    await CallCenterOp_Test.name.set()
    await state.update_data(id=str(message.from_user.id))
    await state.update_data(username=str(message.from_user.username))


@dp.message_handler(state='*', commands='cancel_test')
@dp.message_handler(Text(equals='cancel_test', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Отмена.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=CallCenterOp_Test.name)
async def process_name(message: types.Message, state: FSMContext):
    try:
        int(message.text)
        await message.reply("Введите имя")
        return
    except:
        await state.update_data(name=message.text)
        await CallCenterOp_Test.next()
        await message.reply("Сколько Вам лет?")


@dp.message_handler(lambda message: not message.text.isdigit(), state=CallCenterOp_Test.age)
async def process_age_invalid(message: types.Message):
    return await message.reply("Возраст должен быть числом.\n"
                               "Сколько Вам лет? (только цифры)")


@dp.message_handler(lambda message: message.text.isdigit(), state=CallCenterOp_Test.age)
async def process_age(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой номер телефона.\n"
                         "(Пример: 79841234567)")


@dp.message_handler(lambda message: not message.text.isdigit(), state=CallCenterOp_Test.phone_number)
async def process_number_invalid(message: types.Message):
    return await message.reply("Введите свой номер телефона.\n"
                               "(Пример: 79841234567)")


@dp.message_handler(lambda message: message.text.isdigit(), state=CallCenterOp_Test.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(phone_number=int(message.text))
    await message.answer("Укажите ссылки на ваш профиль в соц. сети.\n")


@dp.message_handler(state=CallCenterOp_Test.links)
async def process_links(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(links=str(message.text))
    await message.answer("Был ли опыт телефонных переговоров с клиентами?")


@dp.message_handler(state=CallCenterOp_Test.question_1)
async def process_question_1(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(question_1=str(message.text))
    await message.answer("С тёплой или холодной базой?")


@dp.message_handler(state=CallCenterOp_Test.question_1_2)
async def process_question_1_2(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(question_1_2=str(message.text))
    await message.answer("Как Вы видите свою идеальную работу?")


@dp.message_handler(state=CallCenterOp_Test.question_2)
async def process_question_2(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(question_2=str(message.text))
    await message.answer("Сколько звонков в день хотели бы совершать?")


@dp.message_handler(state=CallCenterOp_Test.question_2_2)
async def process_question_2_2(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(question_2_2=str(message.text))
    await message.answer(
        "Ситуация: Вы заметили, что близки к тому, что не выполите план и Ваш доход может не оправдаться, Ваши действия?")


@dp.message_handler(state=CallCenterOp_Test.question_3)
async def process_question_3(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(question_3=str(message.text))
    await message.answer("Какой уровень ЗП для Вас приемлем в 1ый месяц работы?")


@dp.message_handler(state=CallCenterOp_Test.question_4)
async def process_question_4(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(question_4=str(message.text))
    await message.answer(
        "Можете ли Вы привести примеры, когда Ваши работодатели вели себя, на Ваш взгляд, некорректно по отношению к сотрудникам?")


@dp.message_handler(state=CallCenterOp_Test.question_5)
async def process_question_5(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(question_5=str(message.text))
    await message.answer("Назовите, пожалуйста, причины, по которым Вы решили уйти с последнего места работы?")


@dp.message_handler(state=CallCenterOp_Test.question_6)
async def process_question_6(message: types.Message, state: FSMContext):
    await CallCenterOp_Test.next()
    await state.update_data(question_6=str(message.text))
    await message.answer("Когда готовы приступить к работе?")


@dp.message_handler(state=CallCenterOp_Test.question_7)
async def process_question_7(message: types.Message, state: FSMContext):
    await state.update_data(question_7=str(message.text))
    logging.info(await state.get_data())
    await message.answer("Спасибо, все данные сохранены.")
    user_data = await state.get_data()
    text = f"ID: {user_data['id']}\n" \
           f"Username: @{user_data['username']}\n" \
           f"Name: {user_data['name']}\n" \
           f"Age: {user_data['age']}\n" \
           f"Номер телефона: {user_data['phone_number']}\n" \
           f"Ссылки на соцсети: {user_data['links']}\n" \
           f"Вопрос 1: {user_data['question_1']}\n" \
           f"Вопрос 2: {user_data['question_1_2']}\n" \
           f"Вопрос 3: {user_data['question_2']}\n" \
           f"Вопрос 4: {user_data['question_2_2']}\n" \
           f"Вопрос 5: {user_data['question_3']}\n" \
           f"Вопрос 6: {user_data['question_4']}\n" \
           f"Вопрос 7: {user_data['question_5']}\n" \
           f"Вопрос 8: {user_data['question_5']}\n" \
           f"Вопрос 9: {user_data['question_6']}\n" \
           f"Вопрос 10: {user_data['question_7']}"
    for admin in admins:
        await bot.send_message(text=text, chat_id=admin)
    await state.finish()



