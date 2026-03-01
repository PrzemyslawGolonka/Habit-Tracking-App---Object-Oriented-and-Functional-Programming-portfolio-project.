import pytest
from habit import Habit
from datetime import datetime, timedelta
from habit_analyser import HabitAnalyser


def test_check_both_streaks():

    habit_1 = Habit(habit_id=1, name='swimming', periodicity='daily', created_at=datetime.now())
    habit_2 = Habit(habit_id=2, name='learning pythong', periodicity='daily', created_at=datetime.now())
    habit_3 = Habit(habit_id=3, name='skincare', periodicity='daily', created_at=datetime.now())
    habit_4 = Habit(habit_id=4, name='gym', periodicity='weekly', created_at=datetime.now())
    habit_5 = Habit(habit_id=5, name='running', periodicity='weekly', created_at=datetime.now())
    habit_6 = Habit(habit_id=6, name='cooking', periodicity='daily', created_at=datetime.now())

    completions_1 = []
    for day in range(28):
        if day in [5, 12]:
            continue
        else:
            completions_1.append(datetime.now() - timedelta(days=day))

    completions_2 = []
    for day in range(28):
        completions_2.append(datetime.now() - timedelta(days=day))

    completions_3 = []
    for day in range(28):
        if day in [8]:
            continue
        else:
            completions_3.append(datetime.now() - timedelta(days=day))

    completions_4 = []
    for week in range(4):
        if week in [2]:
            continue
        else:
            completions_4.append(datetime.now() - timedelta(weeks=week))

    completions_5 = []
    for week in range(4):
        completions_5.append(datetime.now() - timedelta(weeks=week))

    # if there are no completion dates
    completions_6 = []

    assert HabitAnalyser.check_streak(habit_1, completions_1) == 5
    assert HabitAnalyser.longest_streak(habit_1, completions_1) == 15

    assert HabitAnalyser.check_streak(habit_2, completions_2) == 28
    assert HabitAnalyser.longest_streak(habit_2, completions_2) == 28

    assert HabitAnalyser.check_streak(habit_3, completions_3) == 8
    assert HabitAnalyser.longest_streak(habit_3, completions_3) == 19

    assert HabitAnalyser.check_streak(habit_4, completions_4) == 2
    assert HabitAnalyser.longest_streak(habit_4, completions_4) == 2

    assert HabitAnalyser.check_streak(habit_5, completions_5) == 4
    assert HabitAnalyser.longest_streak(habit_5, completions_5) == 4

    assert HabitAnalyser.check_streak(habit_6, completions_6) == 0
    assert HabitAnalyser.check_streak(habit_6, completions_6) == 0
