"""
This is the file containing the main CLI application.
It handles database connection, retrival of data,
user interaction and analysis output.
"""

import questionary
from questionary import Choice
from habit_database import HabitDB
from habit_analyser import HabitAnalyser


def cli():
    db = HabitDB('habits.db')
    questionary.confirm('Hello!\nWelcome to the Habit Tracking App.\nWould you like to start?').ask()

    stop = False

    # runs until a user chooses to the exit the app.
    while not stop:

        # questionary ensures structured menu for the user.
        choice = questionary.select(
            'What would you like to do today?',
            choices=['Create a habit', 'Check habit off', 'Analyse', 'Delete a habit', 'Exit']
        ).ask()

        if choice == 'Create a habit':
            habit_name = questionary.text("What is the name of your habit?").ask()
            habit_periodicity = questionary.select("What is the periodicity of your habit?",
                                                   choices=['daily', 'weekly']).ask()
            db.add_habit(habit_name, habit_periodicity)

        elif choice == 'Check habit off':
            habits = db.list_all_habits()
            if not habits:
                print('There are no habits yet! Please create a habit first!')
                return
            habit_name = questionary.select("Which of the habits would you like to check off?",
                                            choices=[Choice(title=habit.name, value=habit) for habit in habits]).ask()

            check_off_date = questionary.select("Would you like to check the habit off for today or the past date?",
                                                choices=['today', 'past date']).ask()
            if check_off_date == 'today':
                try:
                    db.add_completion(habit_name.id)
                    print('Habit has been successfully checked off!')
                except ValueError as e:
                    print(e)
            else:
                print('Please provide the date in YYYY-MM-DD format.')
                while True:
                    habit_past_completion = questionary.text("When did you complete the habit?").ask()
                    try:
                        db.add_completion(habit_name.id, habit_past_completion)
                        print('Habit has been successfully checked off for that date!')
                        break
                    except ValueError as e:
                        print(e)

        # another questionary structured menu choice for analytics module.
        elif choice == 'Analyse':
            answer = questionary.select(
                'What exactly would you like to do?',
                choices=['Get the list of all habits',
                         'Get habits by periodicity',
                         'Get current streak of a habit',
                         'Get longest streak of a habit',
                         'Get longest streak of all habits',
                         'See completion dates of a habit']).ask()

            if answer == 'Get the list of all habits':
                habits = db.list_all_habits()
                print('This is the current habit list:')
                for habit in habits:
                    print(habit)

            elif answer == 'Get habits by periodicity':
                habit_periodicity = questionary.select("Which periodicity would you like to get habit for?",
                                                       choices=['daily', 'weekly']).ask()
                habits = db.list_habits_by_periodicity(habit_periodicity)
                print(f'This is the current list of {habit_periodicity} habits:')
                for habit in habits:
                    print(habit)

            elif answer == 'Get current streak of a habit':
                habits = db.list_all_habits()
                if not habits:
                    print('There are no habits yet! Please create a habit first!')
                    return
                habit_name = questionary.select("Which habit would you like to get the current streak of?",
                                                choices=[Choice(title=habit.name, value=habit) for habit in habits]).ask()
                completions = db.get_completions(habit_name.id)
                current_streak = HabitAnalyser.check_streak(habit_name, completions)
                print(f'The current streak of habit: {habit_name.name} is {current_streak}.')

            elif answer == 'Get longest streak of a habit':
                habits = db.list_all_habits()
                if not habits:
                    print('There are no habits yet! Please create a habit first!')
                    return
                habit_name = questionary.select("Which habit would you like to get the longest streak of?",
                                                choices=[Choice(title=habit.name, value=habit) for habit in habits]).ask()
                completions = db.get_completions(habit_name.id)
                longest_streak = HabitAnalyser.longest_streak(habit_name, completions)
                print(f'The longest streak of {habit_name.name} is {longest_streak}.')

            elif answer == 'Get longest streak of all habits':
                habits = db.list_all_habits()
                if not habits:
                    print('There are no habits yet! Please create a habit first!')
                    return
                print('Here is the list of all habits with their corresponding longest streaks:')
                for habit in habits:
                    completions = db.get_completions(habit.id)
                    print(f'{habit.name}: {HabitAnalyser.longest_streak(habit, completions)}')

            elif answer == 'See completion dates of a habit':
                habits = db.list_all_habits()
                if not habits:
                    print('There are no habits yet! Please create a habit first!')
                    return
                habit_name = questionary.select("Which habit would you like to check the completion dates for",
                                                choices=[Choice(title=habit.name, value=habit) for habit in habits]).ask()
                completions = db.get_completions(habit_name.id)
                if not completions:
                    print('No completion dates found for this habit!')
                    continue
                else:
                    print(f'Completion dates for {habit_name.name}')
                    for date in completions:
                        print(date)

        elif choice == 'Delete a habit':
            habits = db.list_all_habits()
            if not habits:
                print('There are no habits yet! Please create a habit first!')
                return
            habit_name = questionary.select("Which habit would you like to delete?",
                                            choices=[Choice(title=habit.name, value=habit) for habit in habits]).ask()

            confirmation = questionary.confirm(f"Are you 100% sure that you want to delete '{habit_name}'? "
                                               f"This will remove its data from database.").ask()

            if confirmation:
                db.delete_habit(habit_name.id)
                print(f"You successfully deleted '{habit_name.name}'.")
            else:
                print("Deletion cancelled.")

        # stops the application from running.
        else:
            print('Bye')
            stop = True


if __name__ == '__main__':
    cli()
