import pytest
from habit_database import HabitDB


@pytest.fixture
def db():
    test_db = HabitDB(":memory:")
    test_db.create_tables()
    return test_db


def test_add_habit(db):
    db.add_habit('reading', 'daily')
    all_habits = db.list_all_habits()
    assert len(all_habits) == 1
    assert all_habits[0].name == 'reading'


def test_list_all_habits(db):
    db.add_habit('swimming', 'weekly')
    db.add_habit('cooking', 'daily')
    db.add_habit('reading', 'daily')
    db.add_habit('learning python', 'daily')
    all_habits = db.list_all_habits()
    assert len(all_habits) == 4
    assert all_habits[0].name == 'swimming'
    assert all_habits[1].name == 'cooking'
    assert all_habits[2].name == 'reading'
    assert all_habits[3].name == 'learning python'


def test_list_habits_by_periodicity(db):
    db.add_habit('cooking', 'daily')
    db.add_habit('reading', 'daily')
    db.add_habit('learning python', 'daily')
    db.add_habit('massage', 'weekly')
    db.add_habit('swimming', 'weekly')

    daily_habits = db.list_habits_by_periodicity('daily')
    weekly_habits = db.list_habits_by_periodicity('weekly')

    assert len(daily_habits) == 3
    assert len(weekly_habits) == 2
    assert weekly_habits[0].name == 'massage'
    assert weekly_habits[1].name == 'swimming'


def test_add_completion(db):
    db.add_habit('cooking', 'daily')
    db.add_habit('reading', 'daily')
    all_habits = db.list_all_habits()

    add_date_habit_1 = db.add_completion(all_habits[0].id)
    add_date_habit_2 = db.add_completion(all_habits[1].id, '2026-02-02')

    completions_habit_1 = db.get_completions(all_habits[0].id)
    completions_habit_2 = db.get_completions(all_habits[1].id)

    assert add_date_habit_1 in completions_habit_1
    assert add_date_habit_2 in completions_habit_2


def test_get_completions(db):
    db.add_habit('cooking', 'daily')
    all_habits = db.list_all_habits()
    db.add_completion(all_habits[0].id, '2026-02-02')
    completions = db.get_completions(all_habits[0].id)

    assert len(completions) == 1


def test_get_habit_periodicity(db):
    db.add_habit('cooking', 'daily')
    db.add_habit('swimming', 'weekly')
    all_habits = db.list_all_habits()

    periodicity_habit_1 = db.get_habit_periodicity(all_habits[0].id)
    periodicity_habit_2 = db.get_habit_periodicity(all_habits[1].id)

    assert periodicity_habit_1 == 'daily'
    assert periodicity_habit_2 == 'weekly'


def test_delete_habit(db):
    db.add_habit('cooking', 'daily')
    all_habits = db.list_all_habits()
    db.delete_habit(all_habits[0].id)

    one_habit = db.list_all_habits()

    assert len(one_habit) == 0
