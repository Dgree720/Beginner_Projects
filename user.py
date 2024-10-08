import sqlite3
from datetime import datetime, date
db_path = "CalorieTracker_DB2.sqlite"


class User:
    def __init__(self, name, current_date):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        self.name = name
        self.age = int(cursor.execute("SELECT Age FROM Users WHERE Name = ?", (name,)).fetchall()[0][0])
        self.gender = cursor.execute("SELECT Gender FROM Users WHERE Name = ?", (name,)).fetchall()[0][0]
        self.height = int(cursor.execute("SELECT Height FROM Users WHERE Name = ?", (name,)).fetchall()[0][0])
        self.weight = int(cursor.execute("SELECT Weight FROM Users WHERE Name = ?", (name,)).fetchall()[0][0])
        self.weight_goal = int(cursor.execute("SELECT WeightGoal FROM Users WHERE Name = ?", (name,)).fetchall()[0][0])
        self.activity_level = int(cursor.execute("SELECT ActivityLevel FROM Users WHERE Name = ?", (name,)).fetchall()[0][0])
        self.start_date = cursor.execute("SELECT StartDate FROM Users WHERE Name = ?", (name,)).fetchall()[0][0]
        self.goal_date = cursor.execute("SELECT GoalDate FROM Users WHERE Name = ?", (name,)).fetchall()[0][0]
        self.calorie_goal = int(cursor.execute("SELECT CalorieGoal FROM Users WHERE Name = ?", (name,)).fetchall()[0][0])
        try:
            self.breakfast_cals = int(cursor.execute("SELECT BreakfastCalories FROM Tracking WHERE User = ? AND Date = ?", (name, current_date)).fetchall()[0][0]) 
            self.lunch_cals = int(cursor.execute("SELECT LunchCalories FROM Tracking WHERE User = ? AND Date = ?", (name, current_date)).fetchall()[0][0])
            self.dinner_cals = int(cursor.execute("SELECT DinnerCalories FROM Tracking WHERE User = ? AND Date = ?", (name, current_date)).fetchall()[0][0])
            self.snack_cals = int(cursor.execute("SELECT SnackCalories FROM Tracking WHERE User = ? AND Date = ?", (name, current_date)).fetchall()[0][0])
            self.total_calories_consumed = int(cursor.execute("SELECT TotalCaloriesConsumed FROM Tracking WHERE User = ? AND Date = ?", (name, current_date)).fetchall()[0][0])
            self.remaining_calories = int(cursor.execute("SELECT RemainingCalories FROM Tracking WHERE User = ? AND Date = ?", (name, current_date)).fetchall()[0][0])
        except IndexError:
            self.breakfast_cals = 0
            self.lunch_cals = 0
            self.dinner_cals = 0
            self.snack_cals = 0
            self.total_calories_consumed = 0
            self.remaining_calories = 0


        connection.close()



    def user_profile(self):
        return {"Name": self.name, 
                "Age": self.age,
                "Gender": self.gender, 
                "Height": self.height, 
                "Starting Weight": self.weight, 
                "Weight Goal": self.weight_goal,
                "Activity Level": self.activity_level, 
                "Start Date": self.start_date, 
                "Goal Date": self.goal_date,
                "Calorie Goal": self.calorie_goal}





if __name__ == "__main__":
    name = "Andi"
    current_date = date.today()
    user = User(name, current_date)
    print(user.user_info())






