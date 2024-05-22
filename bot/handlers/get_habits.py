from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.utils import retrieve_habit_help, send_all_habits
from bot.states import HabitNumber

get_habits_router = Router()


@get_habits_router.message(F.text == 'Посмотреть привычки всех пользователей')
async def all_users_habits(message: Message) -> None:
    try:
        await send_all_habits(message)
    except Exception as e:
        print(e)


@get_habits_router.message(F.text == 'Посмотреть привычки')
async def all_habits(message: Message) -> None:
    try:
        await send_all_habits(message)
    except Exception as e:
        print(e)


@get_habits_router.message(F.text == 'Посмотреть одну привычку')
async def retrieve_habit(message: Message, state: FSMContext) -> None:
    text = 'Напишите номер привычки, которую хотите посмотреть конкретнее 💡:'
    await message.answer(text)
    await send_all_habits(message)
    await state.set_state(HabitNumber.retrieve)


@get_habits_router.message(HabitNumber.retrieve)
async def retrieve_habit2(message: Message, state: FSMContext) -> None:
    await state.update_data(habit_number=message.text)
    data = await state.get_data()
    habit_id = int(data["habit_number"])
    await retrieve_habit_help(message, habit_id)
