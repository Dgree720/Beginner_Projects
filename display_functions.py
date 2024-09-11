import os

class DisplayFunctions:
    def __init__(self) -> None:
        pass
    
    def clear_terminal(self):
        os.system("cls")


    def weight_progress_chart(self):
        os.system("termgraph user_progress.txt --color [green]")


    def calorie_graph(self, too_many_cals):
        if too_many_cals:
            os.system("termgraph calorie_consumption.txt --color {red,cyan} --stacked --width 30")
        else:
            os.system("termgraph calorie_consumption.txt --color {green,cyan} --stacked --width 30")