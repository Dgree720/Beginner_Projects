import sqlite3
from datetime import datetime, date
db_path = "CalorieTracker_DB.sqlite"


class User:
    def __init__(self, name,current_date):
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
        """
        self.breakfast_cals = int(cursor.execute("SELECT BreakfastCalories FROM Tracking WHERE User = ? AND Date = ?", (name, current_date)).fetchall()[0][0]) 
        self.lunch_cals = int(cursor.execute("SELECT LunchCalories FROM Tracking WHERE Name = ? AND User = ?", (name, current_date)).fetchall()[0][0])
        self.dinner_cals = int(cursor.execute("SELECT DinnerCalories FROM Tracking WHERE Name = ? AND User = ?", (name, current_date)).fetchall()[0][0])
        self.snack_cals = int(cursor.execute("SELECT SnackCalories FROM Tracking WHERE Name = ? AND User = ?", (name, current_date)).fetchall()[0][0])
        self.total_calories_consumed = self.breakfast_cals + self.lunch_cals + self.dinner_cals + self.snack_cals
        self.remaining_calories = self.calorie_goal - self.total_calories_consumed
        """

        connection.close()



    def user_info(self):
        return {"Name": self.name, "Age": self.age,
                "Gender": self.gender, "Height": self.height, "Weight": self.weight, "Weight Goal": self.weight_goal,
                "Activity Level": self.activity_level, "Start Date": self.start_date, "Goal Date": self.goal_date,
                "Calorie Goal": self.calorie_goal, #"Remaining Calories": self.remaining_calories}





if __name__ == "__main__":
    name = "Andi"
    user = User(name, "2024-09-07")
    print(user.user_info())






