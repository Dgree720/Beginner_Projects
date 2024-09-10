import time
import sqlite3
from datetime import datetime, date
from user_management import get_reg_users
from user_management import add_user
from user_management import request_username
from general_functions import is_new_day

db_path = "CalorieTracker_DB2.sqlite"
#CalorieTracker_DB.sqlite

def add_new_row_if_necessary(user):
    current_date = date.today()
    sorted_dates = get_all_lines(user)
    if is_new_day(get_most_recent_row(sorted_dates), current_date):
        create_new_row(user, current_date)

def get_most_recent_row(sorted_dates):
    if len(sorted_dates) > 0:
        most_recent_row = datetime.strptime(sorted_dates[0], "%Y-%m-%d").date()
    else:
        pass
    return most_recent_row


def get_most_recent_weight(user, current_date) -> tuple:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(f"SELECT Date, CurrentWeight FROM Tracking WHERE User = ? AND CurrentWeight != ? AND Date != ?", (user.name, 0, current_date))
    weigh_ins = cursor.fetchall()

    if(len(weigh_ins)>0): # weigh_ins kann eine leere liste sein (vermeidet index out of bounds in folgezeile)
        most_recent_weight = sorted(weigh_ins)[0][1]
        most_recent_weighin = sorted(weigh_ins)[0][0]
        connection.close()
        return most_recent_weight, most_recent_weighin
    else:
        #print("weigh_ins is ", weigh_ins, " returning None") # just for debugging
        return (None,None) #weil es einen tupel returnen muss



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
    most_recent_weight, most_recent_weighin = get_most_recent_weight(user, current_date)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Tracking (User, DailyCalorieGoal, Date, RemainingCalories, CurrentWeight) VALUES (?,?,?,?,?)",
                   (user.name, user.calorie_goal, current_date.strftime("%Y-%m-%d"), user.calorie_goal, most_recent_weight))
    connection.commit()
    connection.close()



if __name__ == "__main__":
    current_date = date.today()
    user = User("Andi", current_date)
    print(get_most_recent_weight(user))

