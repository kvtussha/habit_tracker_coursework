from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states import UpdateHabit
from asgiref.sync import sync_to_async

from bot.utils import send_all_users_habits, get_one_habit

update_habit_router = Router()


@update_habit_router.message(F.text == 'Обновить привычку')
async def update_habit_start(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    await message.answer("Напишите, пожалуйста, номер привычки, которую хотите обновить")
    await send_all_users_habits(message, tg_id)
    await state.set_state(UpdateHabit.select_habit)


@update_habit_router.message(UpdateHabit.select_habit)
async def select_habit(message: Message, state: FSMContext) -> None:
    habit_id = int(message.text)
    await state.update_data(habit_id=habit_id)
    await message.answer("Введите новое название привычки:")
    await state.set_state(UpdateHabit.title)


@update_habit_router.message(UpdateHabit.title)
async def habit_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await message.answer("Введите новое место выполнения привычки:")
    await state.set_state(UpdateHabit.place)


@update_habit_router.message(UpdateHabit.place)
async def habit_place(message: Message, state: FSMContext) -> None:
    await state.update_data(place=message.text)
    await message.answer("Введите новое время выполнения привычки (HH:MM):")
    await state.set_state(UpdateHabit.time)


@update_habit_router.message(UpdateHabit.time)
async def habit_time(message: Message, state: FSMContext) -> None:
    await state.update_data(time=message.text)
    await message.answer("Введите новое действие привычки:")
    await state.set_state(UpdateHabit.action)


@update_habit_router.message(UpdateHabit.action)
async def habit_action(message: Message, state: FSMContext) -> None:
    await state.update_data(action=message.text)
    await message.answer("Признак приятной привычки (Да или Нет):")
    await state.set_state(UpdateHabit.is_pleasant_habit)


@update_habit_router.message(UpdateHabit.is_pleasant_habit)
async def is_pleasant_habit(message: Message, state: FSMContext) -> None:
    is_pleasant = message.text
    await state.update_data(is_pleasant_habit=is_pleasant)
    if is_pleasant == 'Да':
        await state.update_data(is_useful_habit='Нет', related_habit=None)
        await message.answer("Введите новую периодичность (в днях):")
        await state.set_state(UpdateHabit.frequency)
    else:
        await state.update_data(is_useful_habit='Да')
        await message.answer("Введите ID связанной привычки (если есть) или 'Нет':")
        await state.set_state(UpdateHabit.related_habit)


@update_habit_router.message(UpdateHabit.related_habit)
async def related_habit(message: Message, state: FSMContext) -> None:
    related_habit_id = message.text
    if related_habit_id.lower() == 'нет':
        await state.update_data(related_habit=None)
    else:
        await state.update_data(related_habit=related_habit_id)
    await message.answer("Введите новую периодичность (в днях):")
    await state.set_state(UpdateHabit.frequency)


@update_habit_router.message(UpdateHabit.frequency)
async def habit_frequency(message: Message, state: FSMContext) -> None:
    await state.update_data(frequency=int(message.text))
    await message.answer("Введите новое вознаграждение:")
    await state.set_state(UpdateHabit.reward)


@update_habit_router.message(UpdateHabit.reward)
async def habit_reward(message: Message, state: FSMContext) -> None:
    await state.update_data(reward=message.text)
    await message.answer("Введите новое время на выполнение (в минутах):")
    await state.set_state(UpdateHabit.time_to_complete)


@update_habit_router.message(UpdateHabit.time_to_complete)
async def habit_time_to_complete(message: Message, state: FSMContext) -> None:
    await state.update_data(time_to_complete=int(message.text))
    await message.answer("Признак публичности привычки (Да или Нет):")
    await state.set_state(UpdateHabit.is_public)


@update_habit_router.message(UpdateHabit.is_public)
async def habit_is_public(message: Message, state: FSMContext) -> None:
    await state.update_data(is_public=message.text)
    await message.answer("Подтвердите обновление привычки (Да или Нет):")
    await state.set_state(UpdateHabit.confirmation)


@update_habit_router.message(UpdateHabit.confirmation)
async def habit_confirmation(message: Message, state: FSMContext) -> None:
    if message.text.lower() == 'да':
        data = await state.get_data()
        habit_id = data.get('habit_id')
        habit = await get_one_habit(habit_id)

        habit.title = data.get('title')
        habit.place = data.get('place')
        habit.time = data.get('time')
        habit.action = data.get('action')
        habit.is_pleasant_habit = data.get('is_pleasant_habit')
        habit.is_useful_habit = data.get('is_useful_habit')
        habit.related_habit = data.get('related_habit')
        habit.frequency = data.get('frequency')
        habit.reward = data.get('reward')
        habit.time_to_complete = data.get('time_to_complete')
        habit.is_public = data.get('is_public')

        await sync_to_async(habit.save)()

        await message.answer("Привычка успешно обновлена.")
    else:
        await message.answer("Обновление привычки отменено.")

    await state.clear()
