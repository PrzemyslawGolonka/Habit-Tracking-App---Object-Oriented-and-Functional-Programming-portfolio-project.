class Habit:
    """
    A class representation of a habit.
    Attributes:
        habit_id - unique identifier of a habit
        name - description of a habit f.e. 'swimming'
        periodicity - frequency of a habit
        created_at - date and time when a habit was created
    """
    def __init__(self, habit_id, name, periodicity, created_at):
        self.id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at

    def __str__(self):
        return self.name
