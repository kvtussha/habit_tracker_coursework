from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.utils import delete_habit_help, send_all_habits
from bot.states import HabitNumber

delete_habit_router = Router()


@delete_habit_router.message(F.text == 'Удалить привычку')
async def delete_habit(message: Message, state: FSMContext) -> None:
    text = 'Напишите номер привычки, которую хотите удалить 📌:'
    await message.answer(text)
    await send_all_habits(message)
    await state.set_state(HabitNumber.delete)


@delete_habit_router.message(HabitNumber.delete)
async def delete_habit2(message: Message, state: FSMContext) -> None:
    await state.update_data(habit_number=message.text)
    data = await state.get_data()
    habit_id = int(data["habit_number"])
    await delete_habit_help(message, habit_id)
    await state.clear()
