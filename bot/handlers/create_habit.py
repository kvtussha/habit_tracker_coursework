from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.states import CreateHabit
from bot.utils import get_one_user, get_one_habit, send_all_users_habits

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
    await message.answer('Признак приятной привычки: Да или Нет')
    await state.set_state(CreateHabit.is_pleasant_habit)


@create_habit_router.message(CreateHabit.is_pleasant_habit)
async def is_pleasant_habit(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    await state.update_data(is_pleasant_habit=message.text)
    await message.answer('Это связанная привычка? Если да, введите её ID, если нет, введите "Нет"')
    await send_all_users_habits(message, tg_id)
    await state.set_state(CreateHabit.related_habit)


@create_habit_router.message(CreateHabit.related_habit)
async def related_habit(message: Message, state: FSMContext) -> None:
    related_habit_id = message.text
    if related_habit_id.lower() != 'нет':
        await state.update_data(related_habit=int(related_habit_id))
    else:
        await state.update_data(related_habit=None)
    await message.answer('Периодичность (в днях)')
    await state.set_state(CreateHabit.frequency)


@create_habit_router.message(CreateHabit.frequency)
async def habit_frequency(message: Message, state: FSMContext) -> None:
    await state.update_data(frequency=int(message.text))
    await message.answer('Вознаграждение')
    await state.set_state(CreateHabit.reward)


@create_habit_router.message(CreateHabit.reward)
async def habit_reward(message: Message, state: FSMContext) -> None:
    await state.update_data(reward=message.text)
    await message.answer('Время на выполнение (в минутах)')
    await state.set_state(CreateHabit.time_to_complete)


@create_habit_router.message(CreateHabit.time_to_complete)
async def habit_time_to_complete(message: Message, state: FSMContext) -> None:
    await state.update_data(time_to_complete=int(message.text))
    await message.answer('Признак публичности привычки: Да или Нет')
    await state.set_state(CreateHabit.is_public)


@create_habit_router.message(CreateHabit.is_public)
async def habit_is_public(message: Message, state: FSMContext) -> None:
    await state.update_data(is_public=message.text)
    await finishing_create_habit(message, state)


async def finishing_create_habit(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    user_id = message.from_user.id
    user = await get_one_user(user_id)

    related_habit_ = None
    if data['related_habit']:
        id_related_habit = data['related_habit']
        related_habit_ = await get_one_habit(id_related_habit)
    data["related_habit"] = related_habit_
    await create_habit(
        user=user,
        title=data['title'],
        place=data['place'],
        time=data['time'],
        action=data['action'],
        is_pleasant_habit=data['is_pleasant_habit'],
        related_habit=related_habit_,
        frequency=data['frequency'],
        reward=data['reward'],
        time_to_complete=data['time_to_complete'],
        is_public=data['is_public'])

    await message.answer('Привычка успешно создана! Посмотрите полный список привычек')
    await state.clear()
