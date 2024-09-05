import pandas as pd
import time
import csv
import sqlite3
from datetime import datetime, date
from user import get_reg_users
from user import add_user
from user import request_username


def main():
    user = "Andreas"
    current_date = datetime.today()
    if is_new_day(get_most_recent_row(), current_date):
        create_new_row(user, current_date)



def get_most_recent_row():
    connector = sqlite3.connect("D:\\DataBase\\CalorieTracker_DB.sqlite")
    cursor = connector.cursor()
    cursor.execute(f"SELECT Date FROM DailyCals WHERE User = ?", ("Andreas",))
    rows = cursor.fetchall()
    unpacked_rows = [rows[x][0] for x in range(len(rows))]
    date_objects = sorted([datetime.strptime(row, "%Y-%m-%d").date() for row in unpacked_rows], reverse = True)
    sorted_dates = [date.strftime("%Y-%m-%d") for date in date_objects]
    most_recent_row = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
    return most_recent_row



def is_new_day(most_recent_row, current_date):
    if most_recent_row < current_date:
        return True
    else:
        return False


def create_new_row(user, current_date):
    pass








if __name__ == "__main__":
    main()


