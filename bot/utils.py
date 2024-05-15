from aiogram.types import Message
from aiogram import F


async def get_habits():
    from habit.views import HabitListAPIView
    habits = await HabitListAPIView().get_all_habits()
    return habits


async def send_all_habits(message: Message):
    habits = await get_habits()
    text = 'Ваши привычки 💫:\n'
    for habit in habits:
        text += f'{habit.pk}. {habit.title}\n'
    await message.answer(text)


async def delete_habit_help(message, habit_id):
    from habit.views import HabitDestroyAPIView
    await HabitDestroyAPIView().perform_destroy(habit_id)
    await message.answer('Привычка удалена')
