import pandas as pd
import termgraph
import seaborn as sns
import time
import sqlite3
from rich import print
from datetime import datetime, date
from user_management import get_reg_users
from user_management import add_user
from user_management import request_username
from user import User
import row_management
import general_functions

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
    cursor.execute("SELECT RemainingCalories FROM Tracking WHERE User = ?", (name,))
    remaining_cals = cursor.fetchall()
    connection.close()
    return remaining_cals



def get_progress(name):
    user = User(name)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT Date, CurrentWeight FROM Tracking WHERE User = ? AND CurrentWeight IS NOT NULL", (name,))
    progress = cursor.fetchall()
    connection.close()
    progress = sorted(progress)
    try:
        weight_progress = progress[len(progress)-1][1] - user.weight
        weight_to_go = user.weight_goal - progress[len(progress)-1][1]
    except IndexError:
        weight_progress = 0
        weight_to_go = user.weight_goal - user.weight
    with open("user_progress.txt", "w"):
        pass
    with open("user_progress.txt", "a") as file:
        file.write(f"{user.start_date} {user.weight}\n")
        for x in range(len(progress)):
            try:
                file.write(f"{progress[x][0]} {str(progress[x][1])}\n")
            except IndexError:
                pass
        file.write(f"{str(user.goal_date)} {str(user.weight_goal)}")
    if weight_progress < 0:
        progress_msg = f"Congrats! You lost {abs(weight_progress)} kg so far! Only {abs(weight_to_go)} kg to go :)"
    elif weight_progress > 0:
        progress_msg = f"You gained {abs(weight_progress)} kg. No big deal, you'll get back on track! {abs(weight_to_go)} kg to go :"
    else:
        progress_msg = f"you maintained your weight... carry on. {abs(weight_to_go)} kg to go :)"
    general_functions.weight_progress_chart()
    print(f"\n{progress_msg}")




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
        connection.close()
    else:
        print("_"*75)
        print("\nokay, for each entry, please enter a valid date and weight. Once you're done"
              "\npress ctrl + z to end your entries.")
        while True:
            try:
                while True:
                    try:
                        date = datetime.strptime(input("Date (YYYY-mm-dd): "), "%Y-%m-%d").date()
                        break
                    except ValueError:
                        print("please enter a valid date")
                        continue
                while True:
                    try:
                        weight = int(input("Weight: "))
                        if 29 < weight < 201:
                            break
                        else:
                            print("please enter a valid weight")
                    except ValueError:
                        print("please enter a valid weight")
                        continue
                connection = sqlite3.connect(db_path)
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Tracking (User, Date, CurrentWeight) VALUES (?, ?, ?)",
                               (user, date, weight))
                connection.commit()
                connection.close()
                print("")
                print("_"*75)
                print("")
            except EOFError:
                print(f"\nOkay, {user}! Thanks for updating your progress :) ")
                break


def show_dashboard(user):
    print("_"*75)
    print(" "* 20 , "[bold blue] Welcome to your Dashboard![/bold blue]")
    print("\n")
    print("[bold blue] Progress on your weightloss journey so far[/bold blue]")
    get_progress(user)







def change_profile():
    print("change profile under construction")


def delete_user():
    print("delete profile under construction")



