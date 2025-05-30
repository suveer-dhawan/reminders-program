'''
Name - Suveer Dhawan

This program improves user interaction with the reminders using data.py. We now give users 
the option to take a snapshot of the current database by using "dump to " and create a 
CSV file. 
'''

import data
import datetime

def display_active_reminders():
    '''
    Displays all active reminders using data module's get_active_reminders function
    
    Return:
        list of active reminders 
    '''
    active_reminders = data.get_active_reminders()
    print("ACTIVE REMINDERS")
    
    # Printing them in ascending order of reminder_id
    for idx, reminder in enumerate(active_reminders, 1):
        print(f"{idx}. {reminder['reminder_text']}")
    return active_reminders

def display_future_reminders():
    '''
    Displays all future reminders using data module's get_future_reminders function
    '''
    future_reminders = data.get_future_reminders()

    # Continuing the count from the displayed "active" reminders
    start_idx = len(data.get_active_reminders()) + 1
    print("FUTURE REMINDERS")
    
    for idx, reminder in enumerate(future_reminders, start_idx):
        print(f"{idx}. {reminder['reminder_text']}")

def display_past_reminders():
    '''
    Displays all past reminders using data module's get_past_reminders function
    '''
    past_reminders = data.get_past_reminders()
    print("PAST REMINDERS")
    
    # Displaying past reminders in negative format (-1, -2..)
    for idx, reminder in enumerate(past_reminders, 1):
        print(f"-{idx}. {reminder['reminder_text']}")


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if "__main__" == __name__:

    # Load the reminder data from CSV files
    data.load_database("test_data.csv", "test_active.csv", "test_dismissed.csv")
    active_reminders = display_active_reminders()
    
    while True:
        
        # Taking user input and making it lowercase for functionality
        user_input = input("> ")
        lower_input = user_input.strip().lower()

        # Using if-else conditionals for different user commands
        if lower_input == "quit":
            print("goodbye")
            break

        # Displaying reminders based on input
        elif lower_input == "future reminders":
            display_future_reminders()

        elif lower_input == "active reminders":
            active_reminders = display_active_reminders()

        elif lower_input == "past reminders":
            display_past_reminders()

        # Dismissing a reminder
        elif lower_input.startswith("dismiss "):
            
            reminder_num = int(user_input.strip().split()[1])

            # Check if the reminder number is valid
            if 1 <= reminder_num <= len(active_reminders):
                reminder_id = active_reminders[reminder_num - 1]['reminder_id']
                data.dismiss_reminder(reminder_id)
                
                # Displaying active reminders after dismissing
                active_reminders = display_active_reminders()
            
            else:
                print(f"{reminder_num} is not a valid item from the menu.")

        # Renewing a reminder
        elif lower_input.startswith("renew "):
            
            # unpacking reminder number and time from input
            parts = user_input.split(" at ")
            reminder_num = int(parts[0].strip().split()[1])
            reminder_time = parts[1].strip()

            past_reminders = data.get_past_reminders()
            future_reminders = data.get_future_reminders()
   
            '''
            Using if else conditionals to get reminder id corresponding to user input
            '''         
            # Accounting for negative list index of past reminders
            if reminder_num < 0:
                index = abs(reminder_num)- 1
                if index < len(past_reminders):
                    reminder_id = past_reminders[index]['reminder_id']

                else:
                    print(f"{reminder_num} is not a valid item from the menu.")
                    continue
            
            elif reminder_num > 0:

                # active reminders if input is positive and less than active_reminders index 
                if reminder_num <= len(active_reminders):
                    reminder_id = active_reminders[reminder_num - 1]['reminder_id']

                # future reminders otherwise
                elif reminder_num <= len(active_reminders) + len(future_reminders):
                    index = reminder_num - len(active_reminders) - 1
                    reminder_id = future_reminders[index]['reminder_id']
                
                else:
                    print(f"{reminder_num} is not a valid item from the menu.")
                    continue
                    
            else:
                print(f"{reminder_num} is not a valid item from the menu.")
                continue

            data.renew_reminder(reminder_id, reminder_time)
            active_reminders = display_active_reminders()

        # Setting reminder for now
        elif lower_input.startswith("remind me now "):
            
            prefix_len = len("remind me now ")
            
            # unpacking reminder text from input 
            reminder_text = user_input[prefix_len:].strip()
            
            #Setting reminder and displaying active reminders
            if reminder_text:
                data.set_reminder(reminder_text, data.now.isoformat())
                active_reminders = display_active_reminders()

        # Setting reminder for specified time
        elif lower_input.startswith("remind at "):

            prefix_len = len("remind at ")
            
            # unpacking reminder time and text from input 
            input_text = user_input[prefix_len:].strip().split("'")
            
            reminder_time = input_text[1]
            reminder_text = input_text[2].strip()

            #Setting reminder and displaying active reminders
            if reminder_text:
                data.set_reminder(reminder_text, reminder_time)
                active_reminders = display_active_reminders()

        elif lower_input.startswith("dump to "):

            #unpacking input and filename
            prefix_len = len("dump to ")
            file_name = user_input[prefix_len:].strip()

            data.dump_database(file_name)

            print(f"{file_name} has been written")
        
        # Asking for input again if no valid command is entered
        else:
            continue