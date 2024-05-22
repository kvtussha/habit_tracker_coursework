# Показать все привычки. Пусть выберет конкретную.
# Напишем поле, которое нужно изменить. Меняем и говорим, что теперь все хорошо

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states import CreateHabit, UpdateHabit
from asgiref.sync import sync_to_async

from bot.utils import send_all_habits, retrieve_habit_help

update_habit_router = Router()


@update_habit_router.message(F.text == 'Обновить привычку')
async def update_habit1(message: Message, state: FSMContext) -> None:
    text = 'Напишите номер привычки, которую хотите изменить 💡:'
    await message.answer(text)
    await send_all_habits(message)
    await state.set_state(UpdateHabit.habit_number)


@update_habit_router.message(UpdateHabit.habit_number)
async def update_habit2(message: Message, state: FSMContext) -> None:
    await state.update_data(habit_number=message.text)
    data = await state.get_data()
    habit_id = int(data["habit_number"])
    await retrieve_habit_help(message, habit_id)
    await message.answer('Напишите номер поля, которое хотели бы изменить 💡')
    await state.set_state(UpdateHabit.habit_field_num)


@update_habit_router.message(UpdateHabit.habit_field_num)
async def update_habit2(message: Message, state: FSMContext) -> None:
    await state.update_data(habit_field_num=message.text)
    data = await state.get_data()
    if data["habit_field_num"] == '1':
        await message.answer('Введите новое название привычки')
