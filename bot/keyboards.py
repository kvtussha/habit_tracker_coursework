from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Посмотреть привычки всех пользователей')],
                                     [KeyboardButton(text='Посмотреть свои привычки')],
                                     [KeyboardButton(text='Посмотреть одну привычку')],
                                     [KeyboardButton(text='Создать привычку')],
                                     [KeyboardButton(text='Обновить привычку')],
                                     [KeyboardButton(text='Удалить привычку')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню')

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить контактную информацию',
                                                           request_contact=True)]], resize_keyboard=True,)

authorisation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Регистрация', callback_data='register')],
    [InlineKeyboardButton(text='Авторизация', callback_data='authorisation')],
])
