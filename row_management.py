import time
import sqlite3
from datetime import datetime, date
from user_management import get_reg_users
from user_management import add_user
from user_management import request_username
from user import User
from general_functions import is_new_day

db_path = "CalorieTracker_DB.sqlite"
#CalorieTracker_DB.sqlite

def add_new_row_if_necessary(user):
    current_date = date.today()
    sorted_dates = get_all_lines(user)
    if is_new_day(get_most_recent_row(sorted_dates), current_date):
        create_new_row(user, current_date)



def get_most_recent_row(sorted_dates):
    most_recent_row = datetime.strptime(sorted_dates[0], "%Y-%m-%d").date()
    return most_recent_row


def get_all_lines(user):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(f"SELECT Date FROM Tracking WHERE User = ?", (user.name,))
    rows = cursor.fetchall()
    unpacked_rows = [rows[x][0] for x in range(len(rows))]
    date_objects = sorted([datetime.strptime(row, "%Y-%m-%d").date() for row in unpacked_rows], reverse=True)
    sorted_dates = [date.strftime("%Y-%m-%d") for date in date_objects]
    connection.close()
    return sorted_dates


def create_new_row(user, current_date):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Tracking (User, DailyCalorieGoal, Date, RemainingCalories) VALUES (?,?,?,?)",
                   (user.name, user.calorie_goal, current_date.strftime("%Y-%m-%d"), user.calorie_goal))
    connection.commit()
    connection.close()




if __name__ == "__main__":
    add_new_row_if_necessary("Andi")


