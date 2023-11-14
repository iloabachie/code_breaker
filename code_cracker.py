from methods import *
import random
import datetime

launch()

while True:
    records = load_records()
    records_display()
    if not player_registered:
        player, player_registered = player_capture()
        reset()
    key, num_digits = code_length()
        
    assert isinstance(num_digits, int), f"{num_digits=}, {type(num_digits)}"

    ### Game core ###
    try:
        high_score = records["high_scores"][key][1]
        best_time = records["best_times"][key][1]
    except:
        high_score = best_time = float('inf')
        
    count = 0  # Sets the counter variable for counting steps
    hint_count = 3 if num_digits == 5 else 2 if num_digits == 4 else 1 if num_digits == 3 else 0
    
    pc_code = "".join(random.sample([str(_) for _ in range(10)], num_digits))    

    # Ensures that timer only starts counting when player is ready
    input("\nPress \033[46m'Enter'\033[0m to start Code Cracking: ")
    start = time.time()  # Sets start time
    
    while True:
        attempt = "attempt" if count == 1 else "attempts"
        if hint_count != 0:
            guess = input(f"\nMake a {num_digits}-digit number guess, type hint or type quit: ").strip().lower()
        else:
            guess = input(f"\nMake a {num_digits}-digit number guess or type quit: ").strip().lower()
        if guess.isnumeric() and len(guess) == num_digits and len(set(guess)) == num_digits:
            merge = [len(set(_)) for _ in zip(pc_code, guess)]
            count += 1
            if guess == pc_code:
                break
            elif 1 in merge:
                print(f"\033[32mM A T C H\033[0m: {attempt}= {count} | time= {time_display(time.time() - start)} | hints left= {hint_count}")
            elif len(guess + pc_code) != len(set(guess + pc_code)):
                print(f"\033[33mC L O S E\033[0m: {attempt}= {count} | time= {time_display(time.time() - start)} | hints left= {hint_count}")
            else:
                print(f"\033[31mN O P E\033[0m: {attempt}= {count} | time= {time_display(time.time() - start)} | hints left= {hint_count}")
        elif guess == 'hint' and hint_count != 0:
            hint = input(
                f"Adds {num_digits // 2 } steps and provides a random digit.  Press 'Enter' to proceed or type no to cancel.").strip().lower()
            if hint == 'no':
                print("No hint. Continue...")
            else:
                print('\033[36m')
                hint_index = random.randint(0, num_digits - 1)
                print("|", end="")
                for _ in range(num_digits):
                    if _ != hint_index:
                        print("_", end="|")
                    else:
                        print(pc_code[_], end="|")
                print('\033[0m')
                hint_count -= 1
                count += num_digits // 2
                print(f'\n{attempt}= {count} | time= {time_display(time.time() - start)} | hints left= {hint_count}')
        elif guess == 'hint' and hint_count == 0:
            print("Sorry, you have no more hints")
        elif guess == 'python' and hint_count == 0:
            hint_count = 3 if num_digits == 5 else 2 if num_digits == 4 else 1
            count += hint_count
            print(f'{attempt}= {count} | time= {time_display(time.time() - start)} | hints left= {hint_count}')
        elif guess == 'test':
            count += num_digits
            flashprint(pc_code, delay=0.5, stay=False, flashes=1)
        elif guess == 'time':
            print(time_display(time.time() - start))
        elif guess == 'quit':
            print()
            printing("Exiting game...")
            break
        else:
            print(f"\033[41mGuess Error\033[0m, guess must contain {num_digits} distinct numbers")

    if guess == "quit":
        break
    else:
        end = round(time.time() - start)  # Captures end time
        duration = time_display(end, digits=False)
        animate1 = '#' * len(player) + '\b' * len(player)

        print('\033[32m')
        flashprint("     ***CODE CRACKED***", flashes=4)
        print('\033[0m\r')
        printing(f"Completed in {count} {attempt} and took {duration}"), time.sleep(1.5)

        # Saves only the fastest score or time in JSON file
        if (high_score == 0 or count < high_score):
            records["high_scores"][key] = [player, count]
        if (best_time == 0 or end < best_time):
            records["best_times"][key] = [player, end]

        if (high_score == 0 or count < high_score) and (best_time == 0 or end < best_time):
            print('\033[33m')
            printing(f"MASTER CODE BREAKER!!! {player}, you SMASHED the steps and time records for '{key}'", new_line=False)
            flashtext(f" {player}, you SMASHED the steps and time records for '{key}'", "MASTER CODE BREAKER!!!", index=0, flashes=6)
            print('\033[0m')
        else:
            count_diff, time_diff = count - high_score, end - best_time
            duration = time_display(time_diff, digits=False)
            if high_score == 0 or count < high_score:
                printing(f"**Congratulations {animate1}{player}!!! You broke the steps record for '{key}'")
                print(f"But you missed the time record by {duration}")
            if best_time == 0 or end < best_time:
                printing(f"**Congratulations {animate1}{player}!!! You broke the time record for '{key}'")
                print(f'But you missed the steps record by {count_diff} steps')
            if not (high_score == 0 or count < high_score) and not (best_time == 0 or end < best_time):
                print(f"You missed the record for {key} by {count_diff} steps\nYou missed the time record by {duration}"), time.sleep(1.5)

        if (high_score == 0 or count < high_score) or (best_time == 0 or end < best_time):
            with open('xCodeCracker/records.json', 'w') as file:
                json.dump(records, file, indent=2, sort_keys=True)

    records_display()

    play_again = input("Press 'Enter' to play again or type 'quit' to exit game...").strip().lower()

    if play_again == 'quit':
        break
    os.system('cls')
print('\033[35m')
printing("Thank you for playing CODE BREAKER!!!")
print(f'©{datetime.date.today().year}')
print("\033[0m")
