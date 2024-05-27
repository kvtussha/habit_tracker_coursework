from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    start = State()
    register = State
    auth = State()
    bot_id = State()


class Register(StatesGroup):
    username = State()
    number = State()
    bot_id = State()


class CreateHabit(StatesGroup):
    title = State()
    place = State()
    time = State()
    action = State()
    is_pleasant_habit = State()
    related_habit = State()
    frequency = State()
    reward = State()
    time_to_complete = State()
    is_public = State()

    completion = State()


class UpdateHabit(StatesGroup):
    habit_number = State()
    habit_field_num = State()
    field_name = State()


class HabitNumber(StatesGroup):
    delete = State()
    retrieve = State()
