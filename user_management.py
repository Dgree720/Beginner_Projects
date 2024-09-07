import csv
import sqlite3
from datetime import datetime
from text_generation_functions import TextGenerator
db_path = "CalorieTracker_DB2.sqlite"

text_generator = TextGenerator(generator_type="motivational_quotes")

# Put all functions as methods into User-Class, once figured out
def get_reg_users():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM Users")
    rows = cursor.fetchall()
    reg_users = [user[0] for user in rows]
    connection.close()
    return reg_users


def request_username():
    while True:
        try:
            name = input("Hi! What is your Name?: ").strip().lower().title()
            break
        except ValueError:
            print("Please enter a valid name")
            continue
    return name


def check_user(name, reg_users):
    if name not in reg_users:
        while True:
            try:
                user_cmd = input("Looks like you're not registered yet. Do you want to register? (ys/no): ").strip().lower()
            except ValueError:
                print("mh, i don't understand. Please type 'yes' or 'no'")
            if user_cmd in ["yes", "no"]:
                if user_cmd == "no":
                    quit("Alright then! Have a nice day!")
                elif user_cmd == "yes":
                    return False
            else:
                print("mh, i don't understand. Please type 'yes' or 'no'")
                continue
    else:
        print("_"*75, "\n\n")
        print(f""*20, f"Welcome back {name}!")
        print(text_generator.gen_motivational_text())
    return True


# need to implement
def request_password():
    pass


def add_user(reg_users):
    print("_" * 75)
    print("Glad you want to join our app! :)"
          "\nlets start off with some questions to fill your profile information \n")
    # Name
    while True:
        name = input("What is your Name? ").lower().title()
        if name in reg_users:
            print("sorry, that name is already taken, please try again")
        else:
            break
    # Age
    while True:
        try:
            age = int(input("What is your age? (18-80) "))
            if 18 <= age <= 80:
                break
            else:
                print("Please enter an age between 18 and 80")
        except ValueError:
            print("Please enter a valid number")
    # Gender
    while True:
        gender = input("What is your gender? ").lower()
        if gender not in ["male", "female"]:
            continue
        else:
            break
    # Height
    while True:
        try:
            height = int(input("What is your height in cm? "))
            if 100 <= height <= 250:
                break
            else:
                print("Please enter a height between 100 and 250 cm")
        except ValueError:
            print("Please ander a valid number")
    # Starting weight
    while True:
        try:
            starting_weight = int(input("What is your current weight in kg? "))
            if 40 <= starting_weight <= 200:
                break
            else:
                print("Please enter a weight between 40 and 200 kg")
        except ValueError:
            print("Please ander a valid number")
    # Weight goal
    while True:
        try:
            goal_weight = int(input("What is your goal weight in kg? "))
            if 40 <= goal_weight <= 200:
                break
            else:
                print("Please enter a weight between 40 and 200 kg")
        except ValueError:
            print("Please ander a valid number")
    # Activity level
    while True:
        print("How active are you on a daily basis?"
              "\n1. Sedentary: little or no exercise"
              "\n2. Light: exercise 1-3 time/week"
              "\n3. Moderate: exercise 4-5 times/week"
              "\n4. Active: daily exercise or intense exercise 3-4 times/week"
              "\n5. Very Active: intense exercise 6-7 times a week"
              "\n6. Extra Active very intense exercise daily or physical job")
        try:
            activity_level = int(input("\nWhich of these options are most fitting to you? "))
            if activity_level in [1, 2, 3, 4, 5, 6]:
                break
            else:
                print("please enter a valid number")
        except ValueError:
            print("please enter a valid number")
    # Start date (today)
    start_date = datetime.today().date()
    # End Date
    while True:
        goal_time = input("\nUntil when do you want to reach your goal? (yyyy-mm-dd): ")
        try:
            goal_time = datetime.strptime(goal_time, "%Y-%m-%d").date()
            break
        except ValueError:
            print("mh the format seems to be wrong, please try again")
    # Calorie_goal
    print(f"Your calculated calorie goal is {calc_calorie_gaol(age, gender, height, starting_weight, 
                                                               activity_level, goal_weight, goal_time, start_date)}")
    while True:
        user_cmd = input("Do you want to change that value? (yes/no): ")
        if user_cmd not in ["yes", "no"]:
            continue
        if user_cmd == "yes":
            try:
                calorie_goal = int(input("Okay then, please set your calorie goal: "))
                break
            except ValueError:
                print("please enter a valid number between 1500 and 4000")
        else:
            calorie_goal = calc_calorie_gaol(age, gender, height, starting_weight,
                                             activity_level, goal_weight, goal_time, start_date)
            break
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (Name, Age, Gender, Height, Weight, WeightGoal, ActivityLevel, StartDate, GoalDate, CalorieGoal) VALUES (?,?,?,?,?,?,?,?,?,?)",
                   (name, age, gender, height, starting_weight, goal_weight, activity_level, start_date, goal_time, calorie_goal))
    cursor.execute("INSERT INTO Tracking (User, DailyCalorieGoal, Date, CurrentWeight) VALUES (?,?,?,?)",
        (name, calorie_goal, start_date, starting_weight))
    connection.commit()
    connection.close()
    print(f"\nGreat {name}! Your profile has successfully been added :)")
    print("_"*75)


def is_date(time):
    try:
        datetime.strptime(time, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def calc_calorie_gaol(age, gender, height, starting_weight, activity_level, weight_goal, goal_time, start_date):
    activity_factor = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
        5: 1.725,
        6: 1.9
    }
    if gender == "male":
        BMR = 13.397 * starting_weight + 4.799 * height - 5.677 * age + 88.362
    if gender == "female":
        BMR = 9.247 * starting_weight + 3.098 * height - 4.330 * age + 447.593
    TTDE = BMR * activity_factor[activity_level]
    timeframe = (goal_time - start_date)
    calories_to_lose = (weight_goal - starting_weight) * 7000
    daily_deficit = calories_to_lose / timeframe.days
    calorie_goal = round(TTDE + daily_deficit)
    return calorie_goal

