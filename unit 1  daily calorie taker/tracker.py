import datetime as dt

# Header section
print("\033[1;33m" + "=" * 130 + "\033[0m")
print("\033[1;33m{:^130}\033[0m".format("WELCOME TO DAILY CALORIE TRACKER"))
print("\033[1;33m" + "=" * 130 + "\033[0m")

# Personal info
print("\nSTUDENT NAME: Avijit")
print("ROLL NO: 2501730308")
print(f"DATE: {dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
print()

# Empty lists
meal_names = []
meal_calories = []

# User inputs
total_meals = int(input("ENTER HOW MANY MEALS YOU WANT TO ADD: "))
print()
limit = float(input("ENTER YOUR DAILY CALORIE LIMIT: "))
print()

# Loop for input
for i in range(total_meals):
    entry = input(f"Enter meal {i+1} (name, calories): ").strip()
    meal, cal = entry.split(',')
    meal_names.append(meal.strip().upper())
    meal_calories.append(float(cal.strip()))

# Display table
print("\n\033[1;96m{:<6}{:<25}{:<15}\033[0m".format("S.NO", "MEAL NAME", "CALORIES"))
print("\033[1;96m" + "-" * 50 + "\033[0m")

for i in range(len(meal_names)):
    print("\033[1;96m{:<6}{:<25}{:<15}\033[0m".format(i+1, meal_names[i], meal_calories[i]))

print("\033[1;96m" + "-" * 50 + "\033[0m")

total_cal = sum(meal_calories)
avg_cal = total_cal / len(meal_calories)

print(f"\nTotal Calories Consumed : {total_cal}")
print(f"Average Calories per Meal : {avg_cal:.2f}\n")

# Status check
if total_cal > limit:
    print("⚠ YOU HAVE EXCEEDED YOUR DAILY CALORIE LIMIT.")
else:
    print("✅ YOU ARE WITHIN YOUR DAILY CALORIE LIMIT.")

# Save report option
save = input("\nDo you want to save your report (yes/no)? ").strip().lower()
if save == "yes":
    with open("calorie_log.txt", "w") as f:
        f.write("===== DAILY CALORIE TRACKER REPORT =====\n")
        f.write(f"NAME: Avijit\nROLL NUMBER: 2501730308\nDATE: {dt.datetime.now()}\n\n")
        f.write("{:<6}{:<25}{:<15}\n".format("S.NO", "MEAL NAME", "CALORIES"))
        f.write("-" * 50 + "\n")
        for i in range(len(meal_names)):
            f.write("{:<6}{:<25}{:<15}\n".format(i+1, meal_names[i], meal_calories[i]))
        f.write("-" * 50 + "\n")
        f.write(f"Total Calories Consumed : {total_cal:.2f}\n")
        f.write(f"Average Calories per Meal : {avg_cal:.2f}\n")
        f.write(f"Daily Calorie Limit : {limit:.1f}\n")
        f.write("STATUS : {}\n".format("Exceeded Limit" if total_cal > limit else "Within Limit"))
    print("Report saved successfully.")
else:
    print("Report not saved.")