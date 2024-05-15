from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import bot.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.utils import send_all_habits, delete_habit_help

router = Router()


class Register(StatesGroup):
    username = State()
    number = State()
    bot_id = State()


@router.message(Command('register'))
async def register(message: Message, state: FSMContext) -> None:
    await state.set_state(Register.username)
    await message.answer('Введите Ваше имя')


@router.message(Register.username)
async def register_name(message: Message, state: FSMContext) -> None:
    await state.update_data(username=message.text)
    await state.set_state(Register.number)
    await message.answer('Отправьте Вашу контактную информацию', reply_markup=kb.get_number)


@router.message(Register.number, F.contact)
async def register_bot_id(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.contact.phone_number)
    await state.update_data(bot_id=message.contact.user_id)
    data = await state.get_data()
    await message.answer(
        f'Ваше имя: {data["username"]}\nВаш номер телефона: {data["number"]}\nВаш id: {data["bot_id"]}')
    await state.clear()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = ('Привет 🌿 Меня зовут HabitTrackerBot\n\n'
            'Я - твой надежный помощник в поддержании физического и ментального здоровья 😉\n\n'
            'Трекер привычек поможет тебе следить за отслеживать свой прогресс в достижении целей, '
            'формировать новые полезные привычки и избавляться от вредных 🍎')
    await message.answer(text, reply_markup=kb.main)


@router.message(F.text == 'Посмотреть привычки')
async def all_habits(message: Message) -> None:
    try:
        await send_all_habits(message)
    except Exception as e:
        print(e)


class Delete(StatesGroup):
    habit_number = State()


@router.message(F.text == 'Удалить привычку')
async def delete_habit(message: Message, state: FSMContext) -> None:
    text = 'Напишите номер привычки, которую хотите удалить 📌:'
    await message.answer(text)
    await send_all_habits(message)
    await state.set_state(Delete.habit_number)


@router.message(Delete.habit_number)
async def delete_habit_number(message: Message, state: FSMContext) -> None:
    await state.update_data(habit_number=message.text)
    data = await state.get_data()
    await message.answer(f'{data}')
    habit_id = int(data["habit_number"])
    await delete_habit_help(message, habit_id)

