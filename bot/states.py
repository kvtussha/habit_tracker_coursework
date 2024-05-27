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
    # title = State()
    # place = State()
    # time = State()
    # action = State()
    # is_pleasant_habit = State()
    # related_habit = State()
    # frequency = State()
    # reward = State()
    # time_to_complete = State()
    # is_public = State()
    #
    # completion = State()
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
    confirmation = State()


class UpdateHabit(StatesGroup):
    select_habit = State()
    title = State()
    place = State()
    time = State()
    action = State()
    is_pleasant_habit = State()
    is_useful_habit = State()
    related_habit = State()
    frequency = State()
    reward = State()
    time_to_complete = State()
    is_public = State()
    confirmation = State()


class HabitNumber(StatesGroup):
    delete = State()
    retrieve = State()
