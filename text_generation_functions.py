from random import choice

class TextGenerator():

    def __init__(self,generator_type="motivational_quotes"):
        self.type=generator_type
    
    
    def gen_motivational_text(self):
        with open("motivational_setences.txt","r") as file:
            lines = file.readlines()
            return " " + choice(lines)

