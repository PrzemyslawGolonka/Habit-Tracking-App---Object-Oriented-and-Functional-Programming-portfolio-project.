import sqlite3
from datetime import datetime
from habit import Habit


class HabitDB:
    """
    A class representation of a database functionality.

    It uses SQLite to manage the database two tables:
    - habits table - for storing information about habits
    - completions - for saving completion dates for a given habit.

    It handles database related functionality, such as:
    adding a habit, listing all habits, listing habits by periodicity,
    adding completion date, getting the completion dates, and deleting a habit.
    """

    def __init__(self, db='habits.db'):
        self.db = sqlite3.connect(db)
        self.create_tables()

    def create_tables(self):
        """
        This functino creates two tables:
        - habits - stores habit_id, name, periodicity and creation date.
        - completions - stores id, habit_id and completion dates.
        """
        cur = self.db.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            periodicity TEXT NOT NULL,
            created_at TEXT NOT NULL)
            """)

        cur.execute(""" 
            CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completion_dates TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id))
            """)

        self.db.commit()

    def add_habit(self, name, periodicity):
        """
        The function add_habit adds a habit to a database with its name, periodicity and creation date.
        The function handles a case when a user would like to insert a habit that already exists.
        It takes two parameters:
        :param name: action's description.
        :param periodicity: frequency of a habit, daily or weekly.
        :return: Habit object
        """
        cur = self.db.cursor()
        created_at = datetime.now().isoformat()
        try:
            cur.execute(
                "INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?)",
                (name, periodicity, created_at)
            )
            self.db.commit()
            habit_id = cur.lastrowid
            return Habit(habit_id, name, periodicity, created_at)
        except sqlite3.IntegrityError:
            print('This habit already exists.')
            return None

    def list_all_habits(self):
        """
        This function list_all_habits is used to obtain the list of all habits.
        :return: list of all habit objects.
        """
        cur = self.db.cursor()

        cur.execute("SELECT id, name, periodicity, created_at FROM habits")

        habits = cur.fetchall()

        all_habits = []

        for habit in habits:
            all_habits.append(Habit(habit[0], habit[1], habit[2], habit[3]))
        return all_habits

    def list_habits_by_periodicity(self, periodicity):
        """
        The function list_habits_by_periodicity is used for obtaining all habits with given periodicity,
        f.e. only daily habits.
        :param periodicity: a string, 'daily' or 'weekly'.
        :return: a list of habit objects with given periodicity.
        """
        cur = self.db.cursor()

        cur.execute("SELECT id, name, periodicity, created_at FROM habits WHERE periodicity = ?", (periodicity,))

        periodicities = cur.fetchall()

        habit_periodicities = []

        for periodicity in periodicities:
            habit_periodicities.append(Habit(periodicity[0], periodicity[1], periodicity[2], periodicity[3]))
        return habit_periodicities

    def add_completion(self, habit_id, completion=None):
        """
        The function add_completions adds a single completion date to the completions table for a given habit id.
        It handles cases for adding current and past dates, as well as future dates.
        :param habit_id: id of a habit that the completion date should be added to.
        :param completion: completion date, if no date is provided - it adds the current date.
        """
        cur = self.db.cursor()

        if completion is None:
            completion_date = datetime.now()
        else:
            try:
                completion_date = datetime.fromisoformat(completion)
            except ValueError:
                raise ValueError('Wrong date format! Please provide the date in YYYY-MM-DD format.')
        # future date handling
        if completion_date > datetime.now():
            raise ValueError('Checking off the habit for future dates is not permitted.')
        # checking for double dates
        periodicity = self.get_habit_periodicity(habit_id)

        cur.execute("SELECT completion_dates FROM completions WHERE habit_id = ?", (habit_id,))
        dates = cur.fetchall()
        available_dates = [datetime.fromisoformat(date[0]) for date in dates]

        if periodicity == 'daily':
            for date in available_dates:
                if date.date() == completion_date.date():
                    raise ValueError('Habit has already been checked off for this date!')
        elif periodicity == 'weekly':
            year, week, _ = completion_date.isocalendar()
            for date in available_dates:
                y, w, _ = date.isocalendar()
                if y == year and w == week:
                    raise ValueError('Habit has already been checked off for this week!')

        cur.execute("INSERT INTO completions (habit_id, completion_dates) VALUES (?, ?)",
                    (habit_id, completion_date.isoformat()))

        self.db.commit()
        return completion_date

    def get_completions(self, habit_id):
        """
        The function get_completions lists all the completion dates for a given habit.
        :param habit_id: id of a habit that a user wants to get the completion dates for.
        :return: a list of completion dates (datetime objects) of a habit.
        """
        cur = self.db.cursor()

        cur.execute("SELECT completion_dates FROM completions WHERE habit_id = ? ORDER BY completion_dates",
                    (habit_id,))

        completions = cur.fetchall()
        completion_dates = [datetime.fromisoformat(completion[0]) for completion in completions]
        return completion_dates

    def get_habit_periodicity(self, habit_id):
        cur = self.db.cursor()

        cur.execute("SELECT periodicity FROM habits WHERE id = ?", (habit_id,))
        habit_name = cur.fetchone()
        return habit_name[0] if habit_name else None

    def delete_habit(self, habit_id):
        """
        The function delete_habit simply removes a habit from habit and completion tables with provided habit_id.
        :param habit_id: id of a habit that a user wants to delete.
        """
        cur = self.db.cursor()

        cur.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))

        cur.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

        self.db.commit()
