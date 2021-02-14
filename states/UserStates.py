from aiogram.dispatcher.filters.state import StatesGroup, State


class CallCenterOp_Test(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    links = State()
    question_1 = State()
    question_1_2 = State()
    question_2 = State()
    question_2_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    send = State()