import tracemalloc

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import bot.keyboards as kb
from aiogram.fsm.context import FSMContext

from bot.utils import auth_user, create_user, user_info
from bot.states import Register, UserState

user_router = Router()
tracemalloc.start()


@user_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(UserState.start)
    text = ('Привет 🌿 Меня зовут HabitTrackerBot\n\n'
            'Я - твой надежный помощник в поддержании физического и ментального здоровья 😉\n\n'
            'Трекер привычек поможет тебе следить за отслеживать свой прогресс в достижении целей, '
            'формировать новые полезные привычки и избавляться от вредных 🍎')
    await message.answer(text)
    await message.answer('Выберите команду 💫:\n', reply_markup=kb.authorisation)


@user_router.callback_query(F.data == 'authorisation')
async def auth_user_id(message: Message, state: FSMContext) -> None:
    await state.set_state(UserState.auth)
    await message.answer('Отправьте, пожалуйста, Ваши контактные данные для авторизации:\n',
                         reply_markup=kb.get_number)


# @user_router.message(UserState.auth, F.contact)
# async def auth(message: Message, state: FSMContext) -> None:
#     await state.update_data(bot_id=message.contact.user_id)
#     await message.answer('Подождите, происходит авторизация 🍊')
#     data = await state.get_data()
#     user_id = data["bot_id"]
#     ids = await auth_user()
#     if user_id in ids:
#         await message.answer('Спасибо, авторизация прошла успешно 💥!')
#         await message.answer('Теперь Вы можете пользоваться нашим сервисом 🔥 '
#                              'У Вас появилось меню для просмотра, создания, обновления и удаления привычек',
#                              reply_markup=kb.main)
#     else:
#         await message.answer('К сожалению, аутентификация не удалась. '
#                              'Вам нужно зарегистрироваться на нашем сервисе 🥑')
#         await message.answer('Выберите команду 💫:\n', reply_markup=kb.authorisation)


@user_router.callback_query(F.data == 'register')
async def register(message: Message, state: FSMContext) -> None:
    await state.set_state(Register.username)
    await message.answer('Введите Ваше имя')


@user_router.message(Register.username)
async def register_name(message: Message, state: FSMContext) -> None:
    await state.update_data(username=message.text)
    await state.set_state(Register.number)
    await message.answer('Отправьте Вашу контактную информацию', reply_markup=kb.get_number)


@user_router.message(Register.number, F.contact)
async def register_bot_id(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.contact.phone_number)
    await state.update_data(bot_id=message.contact.user_id)
    data = await state.get_data()
    ids = await auth_user()
    if data["bot_id"] not in ids:
        username = data["username"]
        number = data["number"]
        user_id = data["bot_id"]
        await create_user(username, number, user_id)
        await message.answer(
            f'Ваше имя: {username}\nВаш номер телефона: {number}\nВаш id: {user_id}\n'
            f'Регистрация завершена! 🎉')
        await message.answer('Вы можете пользоваться нашим сервисом 🔥 '
                             'У Вас есть меню для просмотра, создания, обновления и удаления привычек',
                             reply_markup=kb.main)
        await state.clear()
    else:
        await message.answer('Вам не нужна регистрация, вы уже авторизированы)')
        await message.answer('Вы можете пользоваться нашим сервисом 🔥 '
                             'У Вас есть меню для просмотра, создания, обновления и удаления привычек',
                             reply_markup=kb.main)
