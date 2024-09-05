import pandas as pd
import time
import csv
from user import get_reg_users
from user import add_user
from user import request_username



def main():
    reg_users = get_reg_users()
    if not request_username(reg_users):
        add_user(reg_users)
    else:
        pass






if __name__ == "__main__":
    main()