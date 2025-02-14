import json
import time
import os
import platform

KEYS = ("2-DIGITS", "3-DIGITS", "4-DIGITS", "5-DIGITS")
player_registered = False

def clear_terminal():
    match platform.system():
        case "Windows": command = 'cls'
        case _: command = 'clear'
    os.system(command)

def printing(text, delay=0.07, new_line=True, rev=False):
    if not rev:
        for _ in range(len(text)):
            print(text[:_ + 1], end='\r')
            time.sleep(delay)
    if rev:
        for _ in range(len(text)):
            print(text[-1 - _:], end='\r')
            time.sleep(delay)
    if new_line:
        print()


def flashprint(text, flashes=5, delay=0.2, stay=True):
    for _ in range(flashes):
        print(text, end=('\r')), time.sleep(delay)
        print(' ' * len(text), end='\r'), time.sleep(delay)
    if stay:
        print(text)


def flashtext(phrase, text, index=-1, flashes=3, delay=0.2):
    textb = ' ' * len(text)
    for _ in range(flashes):
        print(phrase[:index] + text + phrase[index:],
              end='\r'), time.sleep(delay)
        print(phrase[:index] + textb + phrase[index:],
              end='\r'), time.sleep(delay)
    print(phrase[:index] + text + phrase[index:])


def animate(text, symbol="#"):
    symbol = len(text) * symbol
    flashprint(symbol, flashes=2, stay=False)
    flashprint(text, flashes=2, stay=True)


def time_display(time, digits=True):
    time = round(time)
    minute, sec = divmod(time, 60)
    second = '{:02d}'.format(sec)
    minute1 = "minute" if minute in [0, 1] else "minutes"
    second1 = "second" if sec in [0, 1] else "seconds"
    if digits:
        return f'{minute}:{second}'
    else:
        return f'{minute} {minute1} and {second} {second1}'


def help_text():
    print("=" * 57), time.sleep(0.1)
    print("{:^57}".format("***CLUES***")), time.sleep(0.2)
    print("MATCH: at least one correct digit in the correct position"), time.sleep(0.2)
    print("CLOSE: at least one correct digit but in wrong position"), time.sleep(0.2)
    print("NOPE:  no correct digit in your guess"), time.sleep(0.2)
    flashprint("=" * 57, flashes=1), time.sleep(0.8)
    
    
def launch():
    clear_terminal()
    print('\033[35m')
    printing("{:>40}".format('Welcome to CODE BREAKER'), delay=0.1, new_line=False, rev=True), time.sleep(0.3)
    flashprint("{:^57}".format('Welcome to CODE BREAKER'), delay=0.3, flashes=3), time.sleep(0.3)
    print("{:^57}".format("*" * len('Welcome to CODE BREAKER')))
    print('\033[0m\r')
    help_text()
    print()


def load_records():
    global records
    try:  # Attempts to extract the records dictionary from JSON file
        with open('xCodeCracker/records.json', 'r') as file:
            records = json.load(file)
    except:  # Sets high score and best time to infinity if record does not exist or JSON file absend
        # Sets the dictionary of the records for first time play
        records = {"high_scores": {}, "best_times": {}}
    return records


def records_display():
    print('\033[36m')
    print("{:>34}".format('**Leader Board**')), time.sleep(0.05)
    print('+----------+' + '---------------------+' * 2), time.sleep(0.05)
    print('| {:^8} | {:^19} | {:^19} |'.format('Game', 'Steps Record', 'Time Record')), time.sleep(0.05)
    for key in KEYS:
        try:
            name1, high_score = records["high_scores"][key]
            name2, best_time = records["best_times"][key]
        except:
            name1 = name2 = "--"
            high_score = best_time = 0
        minute, sec = divmod(best_time, 60)
        print('+----------' * 5 + '+'), time.sleep(0.05)
        print(f'| {key:8} | {name1:8} |{high_score:9d} | {name2:8} |{minute:6d}:{sec:02d} |'), time.sleep(0.05)
    print('+----------' * 5 + '+\n'), time.sleep(0.05)
    print('\033[0m')


def player_capture():
    global player, player_registered    
    
    def name_input():
        printing('Enter your name: ', new_line=False)  # Captures player name
        name = input('Enter your name: ').strip()
        if name.isalpha() and len(name) <= 8:
            name = name.capitalize()
            return name
        print("\n\033[31mInvalid name\033[0m. Must be maximum 8 characters and contain only letters\n")
        return name_input()
    
    player = name_input()
    print()
    animate(f'Welcome to Code Breaker {player.upper()}')
    print()
    player_registered = not player_registered   
    return player, player_registered

def reset():
    reset = input("Would you like to reset the Leader board? y/N: ")
    if reset.lower() == 'y':
        confirm = input("  Are you sure? y/N: ")
        if confirm == 'y':
            for rkey in KEYS:
                records["high_scores"][rkey] = ['--', 0]
                records["best_times"][rkey] = ['--', 0]
            with open('xCodeCracker/records.json', 'w') as file:
                json.dump(records, file, indent=2, sort_keys=True)
            time.sleep(0.5)
            flashprint("    ...Records cleared...", flashes=2)
            records_display()
        else:
            flashprint('Records unchanged', flashes=2)
    else:
        print()
        flashprint('Records unchanged', flashes=2)
        print()
    time.sleep(1)


def code_length():
    def length():
        printing("Choose the hidden code length: ", new_line=False)
        num_digits = input("Choose the hidden code length: ").strip()
        if num_digits.isnumeric() and 2 <= int(num_digits) <= 5:
            num_digits = int(num_digits)
            return num_digits
        print("\n\033[31mCode Length Error\033[0m. Choose a number between 2 and 5 inclusive\n")
        return length()
    
    num_digits = length()
    match num_digits:  # Sets the key value for KEY
        case 2: key = KEYS[0]
        case 3: key = KEYS[1]
        case 4: key = KEYS[2]
        case 5: key = KEYS[3]
    print()
    flashtext("You have chosen  ", f"'{key}'")
    return key, num_digits
