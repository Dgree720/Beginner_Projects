import sqlite3
from datetime import datetime, date
db_path = "C:\\Users\\seide\\OneDrive\\CalorieTracker_DB.sqlite"


class User:
    def __init__(self, name):
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
        connection.close()



    def user_info(self):
        return {"Name": self.name, "Age": self.age,
                "Gender": self.gender, "Height": self.height, "Weight": self.weight, "Weight Goal": self.weight_goal,
                "Activity Level": self.activity_level, "Start Date": self.start_date, "Goal Date": self.goal_date,
                "Calorie Goal": self.calorie_goal}



if __name__ == "__main__":
    name = "Andi"
    user = User(name)
    print(user.user_info())






