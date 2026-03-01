class HabitAnalyser:
    """
    This class is used only for analytic purposes.
    It comes with two static methods:
    - check_streak - that calculates the current streak of a given habit
    - longest_streak - that calculates the longest streak of a given habit
    """

    @staticmethod
    def check_streak(habit, completion_dates):
        """
        The function check_streak calculates the current streak of a given habit,
        handling both daily and weekly cases.
        It also takes into account transition of the year in weekly streak calculation.
        It takes two parameters:
        :param habit: takes a habit object as an input
        :param completion_dates: takes a list of completion dates (datetime objects) of a habit
        :return: current streak, an integer
        """
        # handles the case of no completion dates
        if not completion_dates:
            return 0

        new_dates = sorted(set(completion_dates))
        periodicity = habit.periodicity

        if periodicity == 'daily':
            streak = 1
            # to check the 'current' daily streak - most recent dates
            recent_dates = new_dates[::-1]
            for idx in range(1, len(recent_dates)):
                if (recent_dates[idx-1].date() - recent_dates[idx].date()).days == 1:
                    streak += 1
                else:
                    break

            return streak

        elif periodicity == 'weekly':
            streak = 1
            updated_dates_list = []
            # .isocalendar() handles week calculation, also across the years.
            for date in new_dates:
                iso_date = date.isocalendar()
                updated_dates_list.append((iso_date.year, iso_date.week))

            unique_weeks = set(updated_dates_list)
            # to check the 'current' weekly streak
            updated_dates = sorted(list(unique_weeks), reverse=True)

            for idx in range(1, len(updated_dates)):
                cur_year, cur_week = updated_dates[idx-1]
                prv_year, prv_week = updated_dates[idx]

                if cur_year == prv_year:
                    if cur_week - prv_week == 1:
                        streak += 1
                    else:
                        break
                # handles transition between year
                elif cur_year == prv_year + 1:
                    if prv_week in [52, 53] and cur_week == 1:
                        streak += 1
                    else:
                        break
                else:
                    break

            return streak

    @staticmethod
    def longest_streak(habit, completion_dates):
        """
        The function longest_streak calculates the longest existing streak of a given habit,
        handling both daily and weekly cases.
        It also takes into account transition of the year in weekly streak calculation.
        It takes two parameters:
        :param habit: takes a habit object as an input
        :param completion_dates: takes a list of completion dates (datetime objects) of a habit
        :return: longest streak, an integer
        """
        # similar logic to the check_streak function.
        if not completion_dates:
            return 0

        new_dates = sorted(set(completion_dates))
        periodicity = habit.periodicity

        if periodicity == 'daily':
            current_streak = 1
            longest_streak = 1

            for idx in range(1, len(new_dates)):
                if (new_dates[idx].date() - new_dates[idx - 1].date()).days == 1:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1

            return longest_streak

        elif periodicity == 'weekly':
            current_streak = 1
            longest_streak = 1
            updated_dates_list = []

            for date in new_dates:
                iso_date = date.isocalendar()
                updated_dates_list.append((iso_date.year, iso_date.week))

            unique_weeks = set(updated_dates_list)
            updated_dates = sorted(list(unique_weeks))

            for idx in range(1, len(updated_dates)):
                prv_year, prv_week = updated_dates[idx - 1]
                cur_year, cur_week = updated_dates[idx]

                if cur_year == prv_year:
                    if cur_week - prv_week == 1:
                        current_streak += 1
                        longest_streak = max(longest_streak, current_streak)
                    else:
                        current_streak = 1
                # handles edge case of transition of the years
                elif cur_year == prv_year + 1:
                    if prv_week in [52, 53] and cur_week == 1:
                        current_streak += 1
                        longest_streak = max(longest_streak, current_streak)
                    else:
                        current_streak = 1

            return longest_streak
