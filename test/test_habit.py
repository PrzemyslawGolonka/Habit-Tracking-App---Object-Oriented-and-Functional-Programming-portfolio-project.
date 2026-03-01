import pytest
from datetime import datetime
from habit import Habit


def test_check_habit():

    habit = Habit(habit_id=1, name='swimming', periodicity='daily', created_at=datetime.now())

    assert habit.id == 1
    assert habit.name == 'swimming'
    assert habit.periodicity == 'daily'
    assert habit.created_at.date() == datetime.now().date()
