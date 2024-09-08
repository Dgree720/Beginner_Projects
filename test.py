import sqlite3
from datetime import datetime, timedelta
import random

db_path = "CalorieTracker_DB2.sqlite"

first_names = [
    "Alexander", "Benjamin", "Charlotte", "Daniel", "Emma",
    "Felix", "Hannah", "Isabella", "Jakob", "Laura",
    "Leon", "Marie", "Max", "Mia", "Noah",
    "Olivia", "Paul", "Sophie", "Tim", "Zoe"]

last_names = [
    "Becker", "Fischer", "Hoffmann", "Jung", "Kaiser",
    "Klein", "Köhler", "Lehmann", "Maier", "Müller",
    "Neumann", "Richter", "Schmid", "Schneider", "Schulz",
    "Schwarz", "Vogel", "Wagner", "Weber", "Zimmermann"]

#creates sample users for testing

name = f"{random.choice(first_names)} {random.choice(last_names)}"
age = random.randint(18,80)
gender = random.choice(["male", "female"])
height = random.randint(150,200)
weight = random.randint(60,200)
weight_goal = weight - random.randint(5,20)
activity_level = random.randint(1,6)
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  # Startdatum, 7 Tage vor heute
goal_date = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')  # Zieldatum in 90 Tagen
calorie_goal = random.randint(2000, 3000)

# Verbindung zur Datenbank und Einfügen der Daten
def insert_user_data():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # SQL-Abfrage
    cursor.execute("INSERT INTO Users (Name, Age, Gender, Height, Weight, WeightGoal, ActivityLevel, StartDate, GoalDate, CalorieGoal)"
    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
    (name, age, gender, height, weight, weight_goal, activity_level, start_date, goal_date, calorie_goal))

    # Änderungen speichern
    connection.commit()
    connection.close()


def insert_tracking_data():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # SQL-Abfrage
    cursor.execute("INSERT INTO Tracking (User, DailyCalorieGoal, RemainingCalories, CurrentWeight, Date)"
    "VALUES (?, ?, ?, ?, ?)", 
    (name, calorie_goal, calorie_goal, weight, start_date))

    # Änderungen speichern
    connection.commit()
    connection.close()




if __name__ == "__main__":
    try:
        insert_user_data()
        insert_tracking_data()
    except:
        pass


"""
# can be used to delete multiple dummy/ sample entries at once
del_names = ["Max Weber"]

def delete_user_data(del_names):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # SQL DELETE Abfrage
    for name in del_names:
        cursor.execute("DELETE FROM Users WHERE Name = ?", (name,))
        cursor.execute("DELETE FROM Tracking WHERE User = ?", (name,))

    # Änderungen speichern
    connection.commit()
    connection.close()

delete_user_data(del_names)
"""