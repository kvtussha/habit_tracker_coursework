from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states import CreateHabit
from asgiref.sync import sync_to_async


create_habit_router = Router()


@create_habit_router.message(F.text == 'Создать привычку')
async def create_habit(message: Message, state: FSMContext) -> None:
    text = 'В ответ на мои сообщения отправляйте, пожалуйста, поля для Вашей будущей привычки💡'
    await message.answer(text)

    await message.answer('Название привычки')
    await state.set_state(CreateHabit.title)


@create_habit_router.message(CreateHabit.title)
async def habit_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await message.answer('Место выполнения привычки')
    await state.set_state(CreateHabit.place)


@create_habit_router.message(CreateHabit.place)
async def habit_place(message: Message, state: FSMContext) -> None:
    await state.update_data(place=message.text)
    await message.answer('Время выполнения привычки в формате 12:00:00')
    await state.set_state(CreateHabit.time)


@create_habit_router.message(CreateHabit.time)
async def habit_time(message: Message, state: FSMContext) -> None:
    await state.update_data(time=message.text)
    await message.answer('Действие привычки')
    await state.set_state(CreateHabit.action)


@create_habit_router.message(CreateHabit.action)
async def habit_action(message: Message, state: FSMContext) -> None:
    await state.update_data(action=message.text)
    await state.set_state(CreateHabit.is_pleasant_habit)
    await message.answer('Признак приятной привычки: Да или Нет')


@create_habit_router.message(CreateHabit.is_pleasant_habit)
async def is_pleasant_habit(message: Message, state: FSMContext) -> None:
    await state.update_data(is_pleasant_habit=message.text)
    await state.set_state(CreateHabit.related_habit)
    await message.answer('Это связанная привычка?')


@create_habit_router.message(CreateHabit.related_habit)
async def related_habit(message: Message, state: FSMContext) -> None:
    # await state.update_data(related_habit=message.text)
    await state.set_state(CreateHabit.frequency)
    await message.answer('Это связанная привычка?')


@create_habit_router.message(CreateHabit.frequency)
async def habit_frequency(message: Message, state: FSMContext) -> None:
    await state.update_data(frequency=int(message.text))
    await state.set_state(CreateHabit.reward)
    await message.answer('Вознаграждение')


@create_habit_router.message(CreateHabit.reward)
async def habit_reward(message: Message, state: FSMContext) -> None:
    await state.update_data(reward=message.text)
    await state.set_state(CreateHabit.reward)
    await message.answer('Время на выполнение (в минутах)')

# это зацикливается, дальше не переходит


@create_habit_router.message(CreateHabit.time_to_complete)
async def habit_time_to_complete(message: Message, state: FSMContext) -> None:
    await state.update_data(time_to_complete=int(message.text))
    await state.set_state(CreateHabit.is_public)
    await message.answer('Признак публичности привычки: Да или Нет')


@create_habit_router.message(CreateHabit.is_public)
async def habit_time_to_complete(message: Message, state: FSMContext) -> None:
    await state.set_state(CreateHabit.completion)
    await state.update_data(is_public=message.text)


@create_habit_router.message(CreateHabit.completion)
async def finishing_create_habit(message: Message, state: FSMContext) -> None:
    await state.clear()
    data = await state.get_data()


# Создать utils для создания привычки
# отправить сообщение, что привычка создалась. Посмотрите полный список привычек
# related_habit
# user
