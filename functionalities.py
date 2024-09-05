import pandas as pd
import time
import csv
import sqlite3
from datetime import datetime, date
from user import get_reg_users
from user import add_user
from user import request_username

def add_food(user, current_date):
    connector = sqlite3.connect("CalorieTracker_DB.sqlite")
    cursor = connector.cursor()


#This is a test

def add_activity():
    pass


def show_remaining_cals(user):
    connection = sqlite3.connect("D:\\DataBase\\CalorieTracker_DB.sqlite")
    cursor = connection.cursor()
    cursor.execute(f"SELECT RemainingCalories FROM CalorieTracking WHERE User = ?", (user,))
    rows = cursor.fetchall()
    print(f"Your remaining calories for today are {rows[0][0]}")




def view_progress():
    pass


def update_weight_progress():
    pass


def show_dashboard():
    pass