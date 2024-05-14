from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import bot.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from habit.views import HabitViewSet

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


@router.message(F.text == 'Посмотреть все привычки')
async def all_habits(message: Message) -> None:
    text = 'Ваши привычки 💫:\n'
    habits = await HabitViewSet().get_habits()
    for ind, habit in enumerate(habits):
        text += f'{ind}. {habit.title}\n'
    await message.answer(text)
