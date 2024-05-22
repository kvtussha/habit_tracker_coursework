from aiogram.types import Message


async def auth_user():
    from users.views import UserListAPIView
    ids = await UserListAPIView().get_all_bot_ids()
    return ids


async def user_info(data: dict):
    user_dict = data
    return user_dict


async def create_user(username, phone, bot_id):
    from users.views import UserCreateAPIView
    await UserCreateAPIView().create_user(username, phone, bot_id)


async def get_all_habits():
    from habit.views import HabitListAPIView
    habits = await HabitListAPIView().get_all_habits()
    return habits


async def send_all_habits(message: Message):
    habits = await get_all_habits()
    text = 'Привычки всех пользователей 💫:\n'
    for habit in habits:
        text += f'{habit.pk}. {habit.title}\n'
    await message.answer(text)


async def delete_habit_help(message, habit_id):
    from habit.views import HabitDestroyAPIView
    await HabitDestroyAPIView().perform_destroy(habit_id)
    await message.answer('Привычка удалена 🌟')


async def retrieve_habit_help(message, habit_id):
    from habit.views import HabitRetrieveAPIView
    habit = await HabitRetrieveAPIView().perform_retrieve(habit_id)
    text = (f'1. Название привычки: {habit.title}\n'
            f'2. Место выполнения привычки: {habit.place}\n'
            f'3. Время выполнения: {habit.time}\n'
            f'4. Действие: {habit.action}\n'
            f'5. Приятная ли это привычка? {habit.is_pleasant_habit}\n'
            f'6. Связанная ли она? {habit.related_habit}\n'
            f'7. Периодичность (в днях): {habit.frequency}\n'
            f'8. Вознаграждение: {habit.reward}\n'
            f'9. Время на выполнение (в минутах): {habit.time_to_complete}\n'
            f'10.Привычка публичная? {habit.is_public}\n')
    await message.answer(f'Вот Ваша информация о привычке 🌼: \n\n{text}')