import os


def clear_terminal():
    os.system("cls")


def weight_progress_chart():
    os.system("termgraph user_progress.txt --color {green}")