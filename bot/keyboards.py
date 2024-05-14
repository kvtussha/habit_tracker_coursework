from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Посмотреть привычки')],
                                     [KeyboardButton(text='Создать привычку')],
                                     [KeyboardButton(text='Обновить привычку')],
                                     [KeyboardButton(text='Удалить привычку')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню')

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить контактную информацию',
                                                           request_contact=True)]], resize_keyboard=True,)
