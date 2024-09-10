import time
import sqlite3
import json
from rich import print
from datetime import datetime, date
from user_management import get_reg_users
from user_management import add_user
from user_management import request_username
from user import User, UserCalories
import row_management
import general_functions

db_path = "CalorieTracker_DB2.sqlite"



def add_food(user, current_date):
    print(f"\nYou have {user.calories.today_calories["remaining_calories"]} kcal left for today")
    print("You can now add Food for your meal of choice")
    while True:
        try:
            meal = input("Meal (Breakfast/Lunch/Dinner/Snack): ").strip().lower().title()
            if meal in ["Breakfast", "Lunch", "Dinner", "Snack"]:
                break
            else:
                print("Please enter a valid choice of meal")
                continue
        except ValueError:
            print("Please enter a valid choice of meal")
    print(f"\nGreat! you can now enter your food you had as a {meal}"
              "\nfor each food that you add, please also enter the amount in grams"
              "\nonce you're finished enter 'exit' to end adding food to your meal :)\n")
    print("_"*75)
    count = 1
    food_items,amounts,calories = [],[],[]
    food_items_dict = {}
    run_loop = True
    while run_loop:
        while True:
            food_item = input(f"Food Item {count}: ").strip().lower().title()
            if food_item == "Exit":
                run_loop = False
                general_functions.clear_terminal()
                break
            else:
                calories_per_100g = general_functions.get_calorie_info(food_item)
                if calories_per_100g == "not found":
                    print("mh, sorry could'nt find that in our database")
                    continue
                else:
                    food_items.append(food_item)
                    break
            print(f"{food_item} has {calories_per_100g} per 100 grams")
        while run_loop:
            try:
                amount = int(input(f"How much {food_item} do you want to add (in g)?: "))
                amounts.append(amount)
                calorie_food = round(calories_per_100g * (amount/100))
                calories.append(calorie_food)
                print(f"okay, adding {amount}g of {food_item}. This amounts to {calorie_food}kcal\n")
                break
            except ValueError:
                print("please enter a valid amount in grams :)")
                continue
        if food_item != "Exit":
            food_items_dict = {f: [a, c] for f,a,c in zip(food_items,amounts,calories)}
            
        count +=1
    # defining values for all columns that should be updated
    meal_total_cals = 0
    for x in range(len(calories)): meal_total_cals += calories[x]
   
    # pulls current value from meal to account for situation where user overwrites food
    # current_calories_of_meal = current_calories_of_chosen_meal(user, meal)
    # total_cals = total_cals - current_calories_of_meal
    meal_calories = meal +"Calories"
    new_total_calories = current_calories_wo_meal(user, meal) + meal_total_cals
    remaining_cals = user.calorie_goal - new_total_calories 
    # running update
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    sql = f"UPDATE Tracking SET {meal} = ?, {meal_calories} = ?, TotalCaloriesConsumed = ?, RemainingCalories = ? WHERE User = ? AND Date = ?"
    
    food_items_json = json.dumps(food_items_dict)
    
    params = (food_items_json, meal_total_cals, new_total_calories, remaining_cals, user.name, current_date.strftime("%Y-%m-%d"))
    cursor.execute(sql, params)
    connection.commit()
    connection.close()
    print(f"\nGreat, {user.name}! Your food items for {meal} have been added :)")
    print(f"Your remaining calories for today are {remaining_cals} kcal.")

    


def current_calories_wo_meal(user:User, meal):
    current_calories_without_meal = (user.calories.today_calories["breakfast_cals"] + user.calories.today_calories["lunch_cals"] 
    + user.calories.today_calories["dinner_cals"] + user.calories.today_calories["snack_cals"]) - user.calories.today_calories[meal.lower() + "_cals"]
    return current_calories_without_meal


# dont know if adding activity makes sense bc activity level already factored in in calorie calculation
def add_activity(user):
    row_management.add_new_row_if_necessary(user)
    print("Activity addition under construction")

# obsolete? attribute remaining_cals of Class User could be used instead
def show_remaining_cals(user, current_date):
    row_management.add_new_row_if_necessary(user)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT RemainingCalories FROM Tracking WHERE User = ? AND Date = ?", (user.name, str(current_date)))
    remaining_cals = cursor.fetchall()[0][0]
    connection.close()
    return remaining_cals


def get_progress(user, current_date):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT Date, CurrentWeight FROM Tracking WHERE User = ? AND CurrentWeight IS NOT NULL", (user.name,))
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
        for x in range(len(progress)):
            try:
                file.write(f"{progress[x][0]} {str(progress[x][1])}\n")
            except IndexError:
                pass
        file.write(f"{str(user.goal_date)} {str(user.weight_goal)}")
    # checks for dates with missing weigh-ins tracking to remind user to add weigh-in
    most_recent_weight, most_recent_weighin = row_management.get_most_recent_weight(user, current_date)

    if(most_recent_weight and most_recent_weighin):
        missing_weigh_ins = (datetime.strptime(most_recent_weighin, '%Y-%m-%d').date() - current_date).days
        most_recent_weighin = datetime.strptime(most_recent_weighin, '%Y-%m-%d').date()
        if missing_weigh_ins < -2:
            weigh_in_warning = f"\nmh, it looks like you haven't tracked your weight for {abs(missing_weigh_ins)} days between {most_recent_weighin} and today. " \
                    "\nSeeing your weight progress can be motivating. Go to the add weight page to update your progress :)"
        else:
            weigh_in_warning = ""
        if weight_progress < 0:
            progress_msg = f"Congrats! You lost {abs(weight_progress)} kg so far! Only {abs(weight_to_go)} kg to go :)"
        elif weight_progress > 0:
            progress_msg = f"You gained {abs(weight_progress)} kg. No big deal, you'll get back on track! {abs(weight_to_go)} kg to go :"
        else:
            progress_msg = f"you maintained your weight... carry on. {abs(weight_to_go)} kg to go :)"
    
    else:
        return "", ""
    
    return weigh_in_warning, progress_msg


def update_weight_progress(user, current_date):
    # adding row for today's date
    row_management.add_new_row_if_necessary(user)
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
                       (new_weight, user.name, current_date))
        connection.commit()
        connection.close()
        print(f"\nDone :) Thank you {user.name} for updating your weight!")
    else:
        print("_"*75)
        print("\nokay, for each entry, please enter a valid date and weight. Once you're done"
              "\npress ctrl + z to end your entries.")
        while True:
            try:
                while True:
                    try:
                        date = datetime.strptime(input("Date (YYYY-mm-dd): "), "%Y-%m-%d").date()
                        if date < datetime.strptime(user.start_date, "%Y-%m-%d").date():
                            print("please enter a valid date after you're journey started")
                        elif date > current_date:
                            print("can you see the future?! please enter a date in the past")
                        else:
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
                existing_entries = row_management.get_all_lines(user)
                if str(date) in existing_entries: #existing_entries = ["2024-09-08"]
                    cursor.execute("UPDATE Tracking SET CurrentWeight = ? WHERE User = ? AND Date = ?",
                                   (weight, user.name, date))
                    connection.commit()
                else:

                    cursor.execute("INSERT INTO Tracking (User, Date, CurrentWeight) VALUES (?, ?, ?)",
                            (user.name, date, weight))
                connection.commit()
                connection.close()
                print("")
                print("_"*75)
                print("")
            except EOFError:
                general_functions.clear_terminal()
                print(f"\nOkay, {user.name}! Thanks for updating your progress :) ")
                break




def show_dashboard(user, current_date):
    print("_"*75)
    print(" "* 20 , "[bold blue] Welcome to your Dashboard![/bold blue]")
    print("\n")
    title1 = "Progress on your weightloss journey so far:"
    print(f"[bold blue] {title1} [/bold blue]")
    print("_"*(len(title1)+1))
    weigh_in_warning, progress_msg = get_progress(user, current_date)
    general_functions.weight_progress_chart()
    
    if weigh_in_warning != "":
        print("\n",progress_msg)
        print("\n",weigh_in_warning)
        print("\n"*2)

    title2 = "Your day so far:"
    print(f"[bold blue] {title2} [/bold blue]")
    print("_"*(len(title2)+1))
    total_calories_consumed, calorie_goal, too_many_cals = calorie_consumption(user, current_date)
    general_functions.calorie_graph(too_many_cals)
    print(f"{total_calories_consumed} kcal eaten so far... your target is {calorie_goal} kcal")




def calorie_consumption(user, current_date):
    total_calories_consumed = user.calories.today_calories["total_calories_consumed"]
    remaining_calories = user.calories.today_calories["remaining_calories"]
    calorie_goal = user.calorie_goal
    if remaining_calories < 0:
        too_many_cals = True
    else:
        too_many_cals = False
    with open ("calorie_consumption.txt", "w") as file:
        file.write(f"{current_date} {total_calories_consumed} {remaining_calories}")
    return total_calories_consumed, calorie_goal, too_many_cals


