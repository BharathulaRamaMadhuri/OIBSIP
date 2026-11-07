import random
import string
 
MIN_LENGTH = 8
MAX_LENGTH = 128
 
def get_length():
    while True:
        value = input(f"Enter the password length you want {MIN_LENGTH} or more (up to {MAX_LENGTH}): ").strip()
        try:
            length = int(value)
        except ValueError:
            print("Error: Please enter a whole number (example: 12).")
            continue
        if length < MIN_LENGTH:
            print(f"Error: Password length must be at least {MIN_LENGTH}.")
            continue
        if length > MAX_LENGTH:
            print(f"Error: Password length must not be more than {MAX_LENGTH}.")
            continue
        return length
 
 
def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Error: Please enter y or n.")
 
 
def get_character_types():
    while True:
        print("\nChoose the character types to include:")
        chosen = []
        if ask_yes_no("Include uppercase letters (A-Z)?"):
            chosen.append(string.ascii_uppercase)
        if ask_yes_no("Include lowercase letters (a-z)?"):
            chosen.append(string.ascii_lowercase)
        if ask_yes_no("Include numbers (0-9)?"):
            chosen.append(string.digits)
        if ask_yes_no("Include symbols (!@#$...)?"):
            chosen.append(string.punctuation)
 
        if len(chosen) == 0:
            print("Error: No character type selected. Please select at least 2 types.")
        elif len(chosen) == 1:
            print("Error: Only 1 type selected. Please select at least 2 types.")
        else:
            return chosen
 
 
def generate_password(length, character_sets):
    # Step 1: take one character from each chosen type (guarantees every type is used)
    password = [random.choice(chars) for chars in character_sets]
 
    # Step 2: fill the remaining length using all chosen characters
    all_chars = "".join(character_sets)
    for _ in range(length - len(password)):
        password.append(random.choice(all_chars))
 
    # Step 3: shuffle so the guaranteed characters are not always at the start
    random.shuffle(password)
    return "".join(password)
 
def main():
    print("=== Random Password Generator ===")
    while True:
        length = get_length()
        character_sets = get_character_types()
 
        password = generate_password(length, character_sets)
        print(f"\nYour password: {password}\n")
 
        again = ask_yes_no("Generate another password?")
        if not again:
            print("Exiting Password Generator.")
            break
        print()
        
if __name__ == "__main__":
    main()