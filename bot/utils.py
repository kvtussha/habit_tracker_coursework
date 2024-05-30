from aiogram.types import Message


async def auth_user():
    """ Авторизация пользователя"""
    from users.views import UserListAPIView
    ids = await UserListAPIView().get_all_bot_ids()
    return ids


async def get_one_user(user_id: int):
    """ Получение пользователя по его id """
    from users.models import User
    user = User.objects.get(bot_id=user_id)
    return user


async def create_user(username, phone, bot_id):
    """ Создание пользователя """
    from users.views import UserCreateAPIView
    await UserCreateAPIView().create_user(username, phone, bot_id)


async def get_all_habits():
    """ Получение всех привычек """
    from habit.views import HabitListAPIView
    habits = await HabitListAPIView().get_all_habits()
    return habits


async def get_one_habit(habit_id):
    """ Получение одной привычки """
    from habit.views import HabitRetrieveAPIView
    habit = await HabitRetrieveAPIView().perform_retrieve(habit_id)
    return habit


async def retrieve_habit_help(message, habit_id):
    """ Получение одной привычки с подробной информацией о ней """
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


async def create_habit(**kwargs):
    from habit.models import Habit
    habit = Habit(**kwargs)
    habit.save()
    return habit


async def send_all_habits(message: Message):
    habits = await get_all_habits()
    text = 'Привычки всех пользователей 💫:\n'
    for habit in habits:
        text += f'{habit.pk}. {habit.title}\n'
    await message.answer(text)


async def send_all_users_habits(message: Message, user_tg_id):
    from habit.views import HabitListAPIView
    habits = await HabitListAPIView().get_all_user_habits(user_tg_id)
    if habits:
        text = 'Ваши привычки 💫:\n'
        for habit in habits:
            text += f'{habit.pk}. {habit.title}\n'
        await message.answer(text)
    else:
        await message.answer('К сожалению, у Вас пока что нет добавленных привычек')


async def delete_habit_help(message, habit_id):
    from habit.views import HabitDestroyAPIView
    await HabitDestroyAPIView().perform_destroy(habit_id)
    await message.answer('Привычка удалена 🌟')
