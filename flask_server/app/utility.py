from random import choice
from string import ascii_uppercase

def generate_room_code(length, games):

    while True:
        code = ""
        for _ in range(length):
            code += choice(ascii_uppercase)

        if code not in games:
            break
    
    return code