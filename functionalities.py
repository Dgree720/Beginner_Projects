import pandas as pd
import time
import sqlite3
from datetime import datetime, date
from user_management import get_reg_users
from user_management import add_user
from user_management import request_username
from user import User
import row_management

db_path = "C:\\Users\\seide\\OneDrive\\CalorieTracker_DB.sqlite"



def add_food(name, current_date):
    row_management.add_new_row_if_necessary()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    print("Adding foods under construction")


def add_activity():
    row_management.add_new_row_if_necessary()
    print("Activity addition under construction")


def show_remaining_cals(name):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(f"SELECT RemainingCalories FROM Tracking WHERE User = ?", (name,))
    remaining_cals = cursor.fetchall()
    return remaining_cals


def view_progress(name):
    user = name
    user = User(user)
    print(user.height)


def update_weight_progress(user, current_date):
    # adding row for today's date
    row_management.add_new_row_if_necessary()
    while True:
        print("Great! Do you want to..."
              "\n1. add a weight for today"
              "\n2. add weights for days in the past")
        try:
            user_cmd = int(input("Select: "))
        except ValueError:
            print("please enter a valid selection")
            continue
        if user_cmd not in [1, 2]:
            print("please enter a valid selection")
            continue
        else:
            break
    if user_cmd == 1:
        while True:
            try:
                new_weight = int(input(f"\nWeight for {current_date}: "))
            except ValueError:
                print("please enter a valid weight")
            if not 30 < new_weight < 200:
                print("please enter a valid weight")
            else:
                break
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("UPDATE Tracking SET CurrentWeight = ? WHERE User = ? AND Date = ?",
                       (new_weight, user, current_date))
        connection.commit()
    else:
        print("not done")







def show_dashboard():
    print("_"*75)


def change_profile():
    print("change profile under construction")


def delete_user():
    print("delete profile under construction")
