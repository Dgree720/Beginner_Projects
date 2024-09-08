import sqlite3
from datetime import datetime, date
db_path = "CalorieTracker_DB2.sqlite"
from row_management import add_new_row_if_necessary


class User:
    def __init__(self, name):
        self.name = name
        self.login_date =  date.today()
        self.login_date_str = date.today().strftime("%Y-%m-%d")
        self.calories = UserCalories(user_belonging_to=self)
        
    def on_login(self):
        add_new_row_if_necessary(user=self) #creates new tracking record if necessary
        self.fetch_db_user_data()

    def fetch_db_user_data(self):
        
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            self.age = int(cursor.execute("SELECT Age FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0])
            self.gender = cursor.execute("SELECT Gender FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0]
            self.height = int(cursor.execute("SELECT Height FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0])
            self.weight = int(cursor.execute("SELECT Weight FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0])
            self.weight_goal = int(cursor.execute("SELECT WeightGoal FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0])
            self.activity_level = int(cursor.execute("SELECT ActivityLevel FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0])
            self.start_date = cursor.execute("SELECT StartDate FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0]
            self.goal_date = cursor.execute("SELECT GoalDate FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0]
            self.calorie_goal = int(cursor.execute("SELECT CalorieGoal FROM Users WHERE Name = ?", (self.name,)).fetchall()[0][0])

        except IndexError:
            print("Warning, ", self, " failed while trying to fetch user data from the database in function User.fetch_user_data()")

        connection.close()
    

    def update_db_tracking_data(self, attribute_name:str,  update_value, date=None):

        if(date==None):
            date = date.today().strftime("%Y-%m-%d")
            
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute(f"UPDATE Tracking SET {attribute_name} = ?  WHERE User = ? AND Date = ?", (update_value, self.name, date))
        except IndexError:
            print("Warning, ", self, " failed while trying to fetch user data from the database in function User.update_db_tracking_data()")
        connection.commit()
        connection.close()


    def update_db_user_data(self, attribute_name:str,  update_value):

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute(f"UPDATE Users SET {attribute_name} = ?  WHERE User = ?", (update_value, self.name))
        except IndexError:
            print("Warning, ", self, " failed while trying to fetch user data from the database in function User.update_db_user_data()")
        connection.commit()
        connection.close()


    def edit_profile(self, user):
        self.view_profile()
        while True:
            user_cmd = input("\nDo you wish to adjust any of your profile information? (yes/no): ")
            if user_cmd not in ["yes", "no"]:
                continue
            else:
                break
        if user_cmd == "yes":
            print(f"Sure thing, {user.name}. Which information would you like to update? Once you're finished, please enter 'exit': ")
            while True:
                info_to_update = input("Update of: ").strip().lower().title()
                if info_to_update == "exit":
                    break
                if info_to_update not in ['Name', 'Age', 'Gender', 'Height', 'Starting Weight', 'Weight Goal', 'Activity Level', 'Start Date', 'Goal Date', 'Calorie Goal']:
                    print("Please enter a valid profile info to update")
                    continue
                new_value = input("New value: ")
        else:
            pass
        

    def view_profile(self,):
        profile = self.get_user_profile_dict()
        for metric, value in profile.items():
            print(f"\n{metric} -> {value}")


    def delete_user():
        print("delete profile under construction")


    def get_user_profile_dict(self):
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






class UserCalories:
    def __init__(self, user_belonging_to):
        self.today_date = date.today().strftime("%Y-%m-%d")
        self.user = user_belonging_to
        
        
        self.today_calories = self.get_db_user_calories(self.today_date) #IMPORTANT: NOT before self.user is assigned



    def get_db_user_calories(self, date):         
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            breakfast_cals = int(cursor.execute("SELECT BreakfastCalories FROM Tracking WHERE User = ? AND Date = ?", (self.user.name, date)).fetchall()[0][0]) 
            lunch_cals = int(cursor.execute("SELECT LunchCalories FROM Tracking WHERE User = ? AND Date = ?", (self.user.name, date)).fetchall()[0][0])
            dinner_cals = int(cursor.execute("SELECT DinnerCalories FROM Tracking WHERE User = ? AND Date = ?", (self.user.name, date)).fetchall()[0][0])
            snack_cals = int(cursor.execute("SELECT SnackCalories FROM Tracking WHERE User = ? AND Date = ?", (self.user.name, date)).fetchall()[0][0])
            total_calories_consumed = int(cursor.execute("SELECT TotalCaloriesConsumed FROM Tracking WHERE User = ? AND Date = ?", (self.user.name, date)).fetchall()[0][0])
            remaining_calories = int(cursor.execute("SELECT RemainingCalories FROM Tracking WHERE User = ? AND Date = ?", (self.user.name, date)).fetchall()[0][0])
            connection.close()
            return {
                "breakfast_cals": breakfast_cals,
                "lunch_cals": lunch_cals,
                "dinner_cals": dinner_cals,
                "snack_cals": snack_cals,
                "total_calories_consumed": total_calories_consumed,
                "remaining_calories": remaining_calories,
            } 

        except IndexError:
            connection.close()
            return None