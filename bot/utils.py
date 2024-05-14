async def get_habits():
    from habit.views import HabitListAPIView
    habits = await HabitListAPIView().get_all_habits()
    return habits
