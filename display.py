
from user import User
from display_functions import DisplayFunctions
from row_management import add_new_row_if_necessary
import functionalities
display_function = DisplayFunctions()
class Display():
    def __init__(self):
        pass

    
    def menu_options(self,user:User, current_date):
        pos_cmds = {
            1: "View Dashboard",
            2: "Add new weight",
            3: "Add Calories",
            4: "Add Activity",
            5: "Edit User Profile",
            6: "Delete User Profile",
            7: "Exit App"
        }
        print("")
        print("_"*75)
        print("What would you like to do?\n")
        print("Menu:"
            "\n1. View Dashboard"
            "\n2. Add new weight"
            "\n3. Add Calories"
            "\n4. Add Activity"
            "\n5. Edit User Profile"
            "\n6. Delete User Profile"
            "\n7. Exit App")
        while True:
            try:
                user_cmd = int(input("Select: "))
            except ValueError:
                print("please enter a valid selection")
                continue
            if user_cmd not in [1, 2, 3, 4, 5, 6, 7]:
                print("please enter a valid selection")
            else:
                display_function.clear_terminal()
                print(f"\nselected to {pos_cmds[user_cmd]}...\n")
                break
        if user_cmd == 1:
            functionalities.show_dashboard(user, current_date)
            self.menu_options(user, current_date)
        elif user_cmd == 2:
            functionalities.update_weight_progress(user, current_date)
            self.menu_options(user, current_date)
        elif user_cmd == 3:
            functionalities.add_food(user,current_date)
            self.menu_options(user, current_date)
        elif user_cmd == 4:
            functionalities.add_activity(user)
            self.menu_options(user, current_date)
        elif user_cmd == 5:
            user.edit_profile(user)
            self.menu_options(user, current_date)
        elif user_cmd == 6:
            user.delete_user()
            self.menu_options(user, current_date)
        elif user_cmd == 7:
            print("_"*75)
            print(".....quitting.....")
            quit("see you next time :)")
        return user_cmd
