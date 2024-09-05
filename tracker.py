import pandas as pd
import time
import csv
from user_management import get_reg_users
from user_management import add_user
from user_management import request_username
from general_functions import clear_terminal
import functionalities




def main():
    pos_cmds = {
        1: "View Dashboard",
        2: "Add new weight",
        3: "Add Calories",
        4: "Add Activity",
        5: "Edit User Profile",
        6: "Delete User Profile"
    }
    reg_users = get_reg_users()
    while not request_username(reg_users):
        reg_users = get_reg_users()
        add_user(reg_users)
        break
    print("What would you like to do?\n")
    print("Menu:"
          "\n1. View Dashboard"
          "\n2. Add new weight"
          "\n3. Add Calories"
          "\n4. Add Activity"
          "\n5. Edit User Profile"
          "\n6. Delete User Profile")
    while True:
        try:
            user_cmd = int(input("Select: "))
        except ValueError:
            print("please enter a valid selection")
            continue
        if user_cmd not in [1, 2, 3, 4, 5, 6]:
            print("please enter a valid selection")
        else:
            clear_terminal()
            print(f"\nselected {pos_cmds[user_cmd]}...\n")
            break
    if user_cmd == 1:
        functionalities.show_dashboard()
    elif user_cmd == 2:
        functionalities.update_weight_progress(user, current_date)
    elif user_cmd == 3:
        functionalities.add_food()
    elif user_cmd == 4:
        functionalities.add_activity()
    elif user_cmd == 5:
        functionalities.change_profile()
    elif user_cmd == 6:
        functionalities.delete_user()










if __name__ == "__main__":
    main()