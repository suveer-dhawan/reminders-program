# 🔔 Reminder Management System 🔔

This repository contains `data.py`, a Python module designed to manage reminders effectively. It handles the lifecycle of reminders—from creation to dismissal or renewal—and interacts with CSV files for persistent storage.

---
## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [How it Works](#how-it-works)
    * [Data Structures](#data-structures)
    * [Core Functions](#core-functions)
* [Usage](#usage)
* [File Structure](#file-structure)
* [Setting the Current Time (`now`)](#setting-the-current-time-now)
* [Author](#author)

---
## Overview

`data.py` provides the backend for a straightforward reminder system. It manages reminder data through three distinct CSV files: one for core reminder details, one for active schedules, and another for dismissed records. This approach ensures data integrity and a clear separation of concerns.

---
## Features

* **Load Database:** Reads reminder data from three CSV files (`reminders.csv`, `active.csv`, `dismissed.csv`) into memory.
* **Categorize Reminders:**
    * **Active Reminders:** Lists reminders currently due.
    * **Past Reminders:** Tracks reminders that were dismissed after becoming active.
    * **Future Reminders:** Shows reminders scheduled to activate later.
* **Manage Reminders:**
    * **Set New Reminders:** Create new reminders with a specified text and activation date.
    * **Dismiss Reminders:** Mark currently active reminders as dismissed.
    * **Renew Reminders:** Add new future activation times to existing reminders.
* **Dump Database:** Consolidates all reminder data (past, active, future) and writes it back to a single, structured CSV file.


---
## How it Works

The system manages reminder data using global Python lists, each tracking a specific aspect of the reminder's state.

### Data Structures

* `reminders_database`: Stores core reminder details (`reminder_id`, `reminder_text`).
* `reminders_active_database`: Tracks when reminders are set to become active.
* `reminders_dismissed_database`: Records when reminders have been dismissed.

### Core Functions

1.  `load_database(reminders_file, active_file, dismissed_file)`: Initializes data from CSVs.
2.  `get_active_reminders()`: Returns reminders currently due based on `now` and dismissal status.
3.  `get_past_reminders()`: Identifies reminders that were active and later dismissed.
4.  `get_future_reminders()`: Finds reminders scheduled to activate after `now`.
5.  `set_reminder(reminder_text, active_from)`: Creates a new reminder and its initial active entry.
6.  `dismiss_reminder(reminder_id)`: Marks an active reminder as dismissed at `now`.
7.  `renew_reminder(reminder_id, active_from)`: Adds a new future activation time for an existing reminder.
8.  `dump_database(database_file)`: Consolidates and writes all reminders to a single CSV file, sorted by active date.

---
## Usage

To use this module, simply import `data.py` into your Python script and call its functions. Ensure your reminder CSV files are in the same directory or provide their full paths.

```python
import data

# Load your reminder data
data.load_database('reminders.csv', 'active.csv', 'dismissed.csv')

# Get and print currently active reminders
active_reminders = data.get_active_reminders()
for rem in active_reminders:
    print(f"Active: ID {rem['reminder_id']}, Text: {rem['reminder_text']}")

# Set a new reminder
data.set_reminder("Pick up dry cleaning", "2025-06-01 10:00:00")

# Dump all reminders to a new CSV file
data.dump_database('all_reminders_output.csv')
```

---
## File Structure

For the system to operate, ensure these CSV files (even if empty with just headers) are alongside `data.py`:
```
.
├── data.py
├── reminders.csv
├── active.csv
└── dismissed.csv
```

---
## Setting the Current Time (`now`)

The `now` variable is a fixed timestamp within `data.py`:

```python
now = datetime.datetime(2025, 4, 7, 10, 0, 0)
```

This acts as the reference point for categorizing reminders. You would change this value directly in ```data.py``` to simulate different "current" times for testing or specific scenarios.

---
## Author

* **Suveer Dhawan** - [GitHub Profile](https://github.com/suveer-dhawan)
