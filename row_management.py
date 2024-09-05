import pandas as pd
import time
import csv
import sqlite3
from datetime import datetime, date
from user_management import get_reg_users
from user_management import add_user
from user_management import request_username
from user import User

db_path = "C:\\Users\\seide\\OneDrive\\CalorieTracker_DB.sqlite"


def add_new_row_if_necessary():
    user = User("Andi")
    current_date = date.today()
    if is_new_day(get_most_recent_row(), current_date):
        create_new_row(user, current_date)



def get_most_recent_row():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(f"SELECT Date FROM Tracking WHERE User = ?", ("Andi",))
    rows = cursor.fetchall()
    unpacked_rows = [rows[x][0] for x in range(len(rows))]
    date_objects = sorted([datetime.strptime(row, "%Y-%m-%d").date() for row in unpacked_rows], reverse = True)
    sorted_dates = [date.strftime("%Y-%m-%d") for date in date_objects]
    most_recent_row = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
    connection.close()
    return most_recent_row


def is_new_day(most_recent_row, current_date):
    if most_recent_row.date() < current_date:
        return True
    else:
        return False


def create_new_row(user, current_date):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Tracking (User, DailyCalorieGoal, Date) VALUES (?,?,?)",
                   (user.name, user.calorie_goal, current_date.strftime("%Y-%m-%d")))
    connection.commit()
    connection.close()




if __name__ == "__main__":
    add_new_row_if_necessary()


