import os

CENTER = 1
LEFT = 0
RIGHT = 2

def display(text, location=CENTER, bg=""):
    print(end=f"{bg}")
    if location == LEFT:
        spaces = ' ' * (os.get_terminal_size().columns - len(text))
        print(end=f'{text}{spaces}')
    elif location == RIGHT:
        spaces = ' ' * (os.get_terminal_size().columns - len(text) - 1)
        print(end=f'{spaces}{text}')
    else:
        spaces = ' ' * (os.get_terminal_size().columns // 2 - len(text) // 2)
        print(end=f'{spaces}{text}{spaces}')
    print(end="\033[0m")