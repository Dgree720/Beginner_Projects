from datetime import datetime, date
import csv
from user_management import get_reg_users
from user_management import add_user
from user_management import request_username
from user_management import check_user
from user import User
from display import Display


def main():
    display = Display()
    current_date = date.today()
    reg_users = get_reg_users()
    name = request_username()
    while not check_user(name, reg_users):
        add_user(reg_users)
        break
    # create instance of User Class
    user = User(name)
    user.on_login()
    user_cmd = display.menu_options(user, current_date)


# user.breakfast_cals






if __name__ == "__main__":
    main()