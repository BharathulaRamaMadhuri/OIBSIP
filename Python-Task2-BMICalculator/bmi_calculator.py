def get_positive_number(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
        except ValueError:
            print("Error: Please enter a numeric value (example: 65 or 1.72).")
            continue
        if number <= 0:
            print("Error: Value must be greater than zero.")
            continue
        return number


def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obese"


def main():
    print("=== BMI Calculator ===")
    while True:
        weight = get_positive_number("Enter your weight (kg): ")
        height = get_positive_number("Enter your height (m): ")

        while height > 3:
            print("Hint: Height should be in meters (example: 1.75, not 175).")
            height = get_positive_number("Enter your height (m): ")

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        print(f"\nYour BMI : {bmi:.2f}")
        print(f"Category : {category}\n")

        again = input("Calculate again? (y/n): ").strip().lower()
        if again != "y":
            print("Exiting BMI Calculator.")
            break
        
if __name__ == "__main__":
    main()
