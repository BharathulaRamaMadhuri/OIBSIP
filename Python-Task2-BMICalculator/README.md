# BMI Calculator (Python - Beginner Tier)

A command-line Python program that calculates Body Mass Index (BMI) from weight and height and shows the health category.

## Features

- Takes weight (kg) and height (m) from the user
- Calculates BMI = weight / (height²)
- Shows BMI rounded to 2 decimal places
- Categories: Underweight (< 18.5), Normal (18.5 - 24.9), Overweight (25 - 29.9), Obese (>= 30)
- Rejects text, negative values, zero and empty input with a helpful error message
- Shows a hint if height is entered in cm by mistake (for example 175 instead of 1.75)
- Option to calculate again without restarting the program

## How to Run

1. Install Python 3
2. Open a terminal in this folder
3. Run the command: `python bmi_calculator.py`

## How It Works

1. The program asks for weight (kg) and height (m).
2. `get_positive_number()` validates the input. Text, negative values and zero are rejected and the user is asked again.
3. If height is greater than 3, a hint is shown to enter it in meters.
4. `calculate_bmi()` calculates BMI = weight / (height²).
5. `classify_bmi()` decides the category.
6. The BMI (2 decimal places) and category are displayed.
7. The user can calculate again or exit.

## Sample Output

    === BMI Calculator ===
    Enter your weight (kg): 70
    Enter your height (m): 1.75

    Your BMI : 22.86
    Category : Normal

    Calculate again? (y/n): n
    Thank you! Stay healthy.

## Test Cases

| Weight (kg) | Height (m) | BMI | Category |
|---|---|---|---|
| 50 | 1.75 | 16.33 | Underweight |
| 70 | 1.75 | 22.86 | Normal |
| 80 | 1.75 | 26.12 | Overweight |
| 100 | 1.75 | 32.65 | Obese |
| abc | - | Error message, asks again | - |
| -5 | - | Error message, asks again | - |
| 70 | 0 | Error message, asks again | - |

## Screenshots

Screenshots of the program running are included in this folder.
The full output of all test cases is available in `bmi_test_output.txt`.

## Author

Bharathula Rama Madhuri

Oasis Infobyte Internship - Python Programming (Task 2)