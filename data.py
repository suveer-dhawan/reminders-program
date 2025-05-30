'''
Name - Suveer Dhawan

This program provides access to the reminders data. We have functions to load the database,
and get active, past, or future reminders from it. We also create functionality for setting
and dismissing reminders, renewing reminders, and dumping the database to a CSV file. 
'''

import csv
import datetime

# Set the current date and time for the program
now = datetime.datetime(2025, 4, 7, 10, 0, 0)

# These lists store reminders and their statuses
reminders_database = []          # Holds reminder texts
reminders_active_database = []   # Holds active reminder times
reminders_dismissed_database = [] # Holds times when reminders were dismissed

def load_database(reminders_file, active_file, dismissed_file):
    """Loads reminders, active times, and dismissed times from CSV files."""
    
    global reminders_database, reminders_active_database, reminders_dismissed_database
    
    # Load the main reminders from the specified file
    with open(reminders_file, mode='r', newline='') as rem_file:
        reader = csv.reader(rem_file)
        reminders_database = []
        next(reader)  # Skip the header row
        
        # Unpacking each row from the file using for loop
        for row in reader:
            reminder_id = int(row[0])  # Unique ID for each reminder
            reminder_text = row[1]      # The actual reminder text
            
            reminders_database.append({
                'reminder_id': reminder_id,
                'reminder_text': reminder_text
            })
    
    # Load the active reminder times from the specified file
    with open(active_file, mode='r', newline='') as act_file:
        reader = csv.reader(act_file)
        reminders_active_database = []
        next(reader)  # Skip the header row
        
        # Unpacking each row from the file
        for row in reader:
            entry_id = int(row[0])          # Unique ID for the entry
            reminder_id = int(row[1])       # ID of the reminder
            active_from = datetime.datetime.fromisoformat(row[2])  # When the reminder becomes active
            
            reminders_active_database.append({
                'entry_id': entry_id,
                'reminder_id': reminder_id,
                'active_from': active_from
            })
    
    # Load the dismissed reminder times from the specified file
    with open(dismissed_file, mode='r', newline='') as dis_file:
        reader = csv.reader(dis_file)
        reminders_dismissed_database = []
        next(reader)  # Skip the header row
        
        # Unpacking each row from the file
        for row in reader:
            entry_id = int(row[0])            # Unique ID for the entry
            reminder_id = int(row[1])         # ID of the reminder
            dismissed_at = datetime.datetime.fromisoformat(row[2])  # When the reminder was dismissed
            
            reminders_dismissed_database.append({
                'entry_id': entry_id,
                'reminder_id': reminder_id,
                'dismissed_at': dismissed_at
            })

def get_active_reminders():
    """Returns a list of reminders that are currently active."""
    
    active_reminders = []
    
    for reminder in reminders_database:
        reminder_id = reminder['reminder_id']
        reminder_text = reminder['reminder_text']
        
        # Check when the reminder was last activated
        active_times = [
            entry for entry in reminders_active_database 
            if entry['reminder_id'] == reminder_id and entry['active_from'] <= now
        ]

        # Check if the reminder has been dismissed
        dismissed_times = [
            entry for entry in reminders_dismissed_database 
            if entry['reminder_id'] == reminder_id and
            entry['dismissed_at'] <= now
        ]

        # Determine if the reminder is still active by comparing latest active from and dismissed entries 
        if active_times and (not dismissed_times or active_times[-1]['active_from'] > dismissed_times[-1]['dismissed_at']):

            # Initializing value for active from and appending to list
            active_from = max(entry['active_from'] for entry in active_times)
            active_reminders.append({
                'reminder_id': reminder_id,
                'reminder_text': reminder_text,
                'active_from': active_from
            })
    
    return active_reminders

def get_past_reminders():
    """Returns a list of reminders that have been dismissed in the past."""
    
    past_reminders = []
    
    for reminder in reminders_database:
        reminder_id = reminder['reminder_id']
        reminder_text = reminder['reminder_text']
        
        # Creating dismissed_times list for comparison
        dismissed_times = [
            entry for entry in reminders_dismissed_database 
            if entry['reminder_id'] == reminder_id and
            entry['dismissed_at'] <= now
        ]

        # Creating active_times list to update values
        active_times = [
            entry for entry in reminders_active_database 
            if entry['reminder_id'] == reminder_id 
            and entry['active_from'] <= now
        ]

        # If the reminder has been dismissed
        if dismissed_times:
            if dismissed_times[-1]['dismissed_at'] > datetime.datetime.fromtimestamp(0):
                
                # Initializing values and appending to past reminders list
                dismissed_at = max(entry['dismissed_at'] for entry in dismissed_times)
                active_from = max(entry['active_from'] for entry in active_times)
                
                past_reminders.append({
                    'reminder_id': reminder_id,
                    'reminder_text': reminder_text,
                    'active_from': active_from,
                    'dismissed_at': dismissed_at
                })
    
    return past_reminders

def get_future_reminders():
    """Returns a list of reminders that are scheduled to become active in the future."""
    
    future_reminders = []
    
    for reminder in reminders_database:
        reminder_id = reminder['reminder_id']
        reminder_text = reminder['reminder_text']
        
        future_entries = [
            entry for entry in reminders_active_database 
            if entry['reminder_id'] == reminder_id and entry['active_from'] > now
        ]

        #Gathering dismissed times 
        dismissed_times = [
            entry for entry in reminders_dismissed_database 
            if entry['reminder_id'] == reminder_id
        ]
        
        # If the reminder is scheduled to be active later, add it to future reminders
        if future_entries:
            
            #Initializing values and appending to future reminders list
            active_from = min(entry['active_from'] for entry in future_entries)
            
            if dismissed_times: 
                latest_dismissed = max(entry['dismissed_at'] for entry in dismissed_times)
                
                # Setting dismissed at dismissed time if its in the future of active_from, else default
                if latest_dismissed > active_from:
                    dismissed_at = latest_dismissed
                else:
                    dismissed_at = datetime.datetime.fromtimestamp(0)

            else:
                dismissed_at = datetime.datetime.fromtimestamp(0)
            
            future_reminders.append({
                'reminder_id': reminder_id,
                'reminder_text': reminder_text,
                'active_from': active_from,
                'dismissed_at': dismissed_at
            })
    
    return future_reminders
def set_reminder(reminder_text, active_from):
    """Set a new reminder."""
    
    global reminders_database
    
    # Setting new reminder_id as largest in the Reminders database + 1
    new_reminder_id = max(
        (reminder['reminder_id'] for reminder in reminders_database),
        default=-1
    ) + 1 
    
    reminders_database.append({
        'reminder_id': new_reminder_id,
        'reminder_text': reminder_text,
    })

     # Setting new entry_id as largest in the Active database + 1
    new_entry_id = max(
        (entry['entry_id'] for entry in reminders_active_database),
        default=-1
    ) + 1 

    reminders_active_database.append({
        'entry_id': new_entry_id,
        'reminder_id': new_reminder_id,
        'active_from': datetime.datetime.fromisoformat(active_from),
    })

def dismiss_reminder(reminder_id):
    """Dismiss the reminder identified by reminder_id."""
    
    past_reminders = get_past_reminders()
    past_reminder_ids = [past_rem['reminder_id'] for past_rem in past_reminders]
    
    for reminder in reminders_database:
        
        # Using conditional for present reminders
        if reminder['reminder_id'] == reminder_id and reminder_id not in past_reminder_ids:

            # Setting new entry_id as largest in the Dismissed database + 1
            new_entry_id = max(
                (entry['entry_id'] for entry in reminders_dismissed_database),
                default=-1
            ) + 1 

            dismissed_at = now  # When the reminder was dismissed            
            reminders_dismissed_database.append({
                'entry_id': new_entry_id,
                'reminder_id': reminder_id,
                'dismissed_at': dismissed_at
            })
            
            break


def renew_reminder(reminder_id, active_from):
    """Renew the reminder identified by reminder_id."""

    global reminders_database

    for reminder in reminders_database:

        if reminder["reminder_id"] == reminder_id:

            # Setting new entry_id as largest in the Active database + 1
            new_entry_id = max(
                (entry['entry_id'] for entry in reminders_active_database),
                default=-1
            ) + 1 

            reminders_active_database.append({
                'entry_id': new_entry_id,
                'reminder_id': reminder_id,
                'active_from': datetime.datetime.fromisoformat(active_from),
            })

            break


def dump_database(database_file):
    """ Writes all reminders "past", "present", and "future" to the database_file in CSV format"""

    all_reminders_to_dump = []
    
    past_reminders = get_past_reminders()
    active_reminders = get_active_reminders()
    future_reminders = get_future_reminders()

    # Adding past, present and future reminders to main list
    for past_rem in past_reminders:
        all_reminders_to_dump.append({
            'reminder_id': past_rem['reminder_id'],
            'reminder_text': past_rem['reminder_text'],
            'active_from': past_rem['active_from'],
            'dismissed_at': past_rem['dismissed_at']
        })

    #Present
    for active_rem in active_reminders:
        all_reminders_to_dump.append({
            'reminder_id': active_rem['reminder_id'],
            'reminder_text': active_rem['reminder_text'],
            'active_from': active_rem['active_from'],
            'dismissed_at': datetime.datetime.fromtimestamp(0) # Active reminders aren't dismissed right now
        })

    active_rem_ids = [active_rem['reminder_id'] for active_rem in active_reminders]

    #Future
    for future_rem in future_reminders:
        future_rem_id = future_rem['reminder_id']

        # adding ones that are not present, to avoid duplicates
        if future_rem_id not in active_rem_ids:
            all_reminders_to_dump.append({
                'reminder_id': future_rem['reminder_id'],
                'reminder_text': future_rem['reminder_text'],
                'active_from': future_rem['active_from'],
                'dismissed_at': future_rem['dismissed_at'] # This should be 1970 timestamp from get_future_reminders
            })


    # Sorting reminders reminders on the basis of active_from and reminder id
    all_reminders_to_dump.sort(key=lambda x: x['active_from'])

    # Set up the headers for your CSV file.
    headers = ['reminder_id', 'reminder_text', 'active_from', 'dismissed_at']

    # Opening file path and adding header
    with open(database_file, 'w', newline= '') as data_file:
        dump_file = csv.writer(data_file)
        dump_file.writerow(headers)

        for rem_data in all_reminders_to_dump:
            dump_file.writerow([
                rem_data['reminder_id'],
                rem_data['reminder_text'],
                rem_data['active_from'].isoformat(sep=' '),
                rem_data['dismissed_at'].isoformat(sep=' ')
            ])