import datetime as dt
print("\033[1;33m[============================================================= WELCOME =============================================================]\033[0m")
print("\033[1;33m[======================================================= DAILY CALORIE TRACKER =======================================================]\033[0m")

print()
print("NAME : Avijit")  # about me
print("ROLL NUMBER : 2501730308")
print(f"DATE : {dt.datetime.now()}") 
print()

meals=[]   # empty list to store meals name
calories=[] # empty list to store calories

user_input = int(input("How many meals do you want to add :".upper())) #ask from user number of meals

print()
user_intake_limit=float(input("Enter your daily calorie limit :".upper())) #ask from user daily calorie limit

print()

count = 0
while count < user_input:  #use while loop to add meals and calories
    user_input1 = input("Enter meal name and calories separated by a comma: ").strip() #ask from user meal name and calories , use strip function to remove extra spaces
    temp_list = user_input1.split(',') #split the input string into meal name and calories
    meals.append(temp_list[0].strip().upper()) #add meal name to meals list after removing extra spaces and converting to uppercase
    calories.append(float(temp_list[1].strip())) #add calories to calories list after converting it to float
    count += 1
 
print()


print("\033[1;96m" + f"{'S NO':<4}{'MEAL NAME':<20}{'CALORIES':<25}" + "\033[0m")  

print("\033[1;96m" + "-" * 50 + "\033[0m")

for i in range(len(meals)):  #
    print("\033[1;96m" + f"{i+1:<4}{meals[i]:<20}{calories[i]:<25}" + "\033[0m")

print("\033[1;96m" + "-" * 50 + "\033[0m")

print("\033[1;96m" + f"Total Calories Consumed : {sum(calories)}" + "\033[0m")

print()
print()
average_calories = sum(calories)/len(calories) #calculate average calories

print(f"Average Calories per Meal : {average_calories:.2f}")
print()

if float(sum(calories)) > user_intake_limit: #compare total calories with user intake limit
    print("You have exceeded your daily calorie limit.".upper())
else:
    print("You are within your daily calorie limit.".upper())

print()



save_choice = input("\nDo you want to save this session report? (yes/no): ").strip().lower()

if save_choice == "yes":
    
    with open("calorie_log.txt", "w") as file:
        file.write("===== DAILY CALORIE TRACKER REPORT =====\n")
        file.write(f"NAME: Avijit\n")
        file.write(f"ROLL NUMBER: 2501730308\n")
        file.write(f"DATE: {dt.datetime.now()}\n\n")

        file.write(f"{'S NO':<4}{'MEAL NAME':<20}{'CALORIES':<25}\n")
        file.write("-" * 40 + "\n")

        for i in range(len(meals)):
            file.write(f"{i+1:<4}{meals[i]:<20}{calories[i]:<25}\n")

        file.write("-" * 40 + "\n")
        file.write(f"Total Calories Consumed: {sum(calories):.1f}\n")
        file.write(f"Average Calories per Meal: {average_calories:.2f}\n")
        file.write(f"Daily Calorie Limit: {user_intake_limit:.1f}\n")

        if sum(calories) > user_intake_limit:
            file.write("STATUS: You exceeded your daily calorie limit.\n")
        else:
            file.write("STATUS: You are within your daily calorie limit.\n")

    print("\nSession report saved successfully as 'calorie_log.txt'")
else:
    print("\nReport not saved.session ended")  
  
  
  