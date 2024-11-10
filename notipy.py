#!/usr/bin/env python3

import sqlite3
import time
import argparse
import os
from datetime import datetime

home_dir = os.path.expanduser("~")
DB_FILE = os.path.join(home_dir, ".config", "notipy", "notipy.db")

def add_reminder(message, notify_time, reminder_type='single'):
    try:
        notify_dt = datetime.strptime(notify_time, "%Y-%m-%d %H:%M:%S")
    except:
        print("Notify time must be in the format 'YYYY-MM-DD HH:MM:SS'")
        return

    #if notify_dt < datetime.now():
    #    print("Notify time must be in the future")
    #    return

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reminders (message, notify_time, add_time, reminder_type) VALUES (?, ?, ?, ?)
        ''', (message, notify_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reminder_type))
        conn.commit()
    
    print(f"Added reminder: '{message}' for {notify_time}")

def remove_reminder(reminder_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
       
        cursor.execute('SELECT * FROM reminders')
        reminders = cursor.fetchall()
        if reminders:
            cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
            conn.commit()
            print(f"Removed reminder: ID = {reminder_id}")
        print(f"No reminder: ID = {reminder_id}")

def list_reminders():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reminders')
        reminders = cursor.fetchall()
        
        print(f"\n\n{'ID':<5} {'Title':<20} {'Notify At':<20} {'Created At':<20} {'Type':<10}")
        print("-" * 75)
        
        if reminders:
            for reminder in reminders:
                print(f"{reminder[0]:<5} {reminder[1]:<20} {reminder[2]:<20} {reminder[3]:<20} {reminder[4]:<10}")
        else:
            print("No active reminders.")

def main():
    parser = argparse.ArgumentParser(description='Manage Reminders')
    
    parser.add_argument('--add', 
                    metavar=('message', 'time'), 
                    nargs=2, 
                    help='Add a reminder with the required message and time.')

    parser.add_argument('--type', 
                    choices=['single', 'daily', 'weekly'], 
                    default='single',
                    help='Reminder type: "single" (default), "daily", or "weekly".')

    parser.add_argument('--remove', type=int, help='Remove a reminder by ID')
    
    parser.add_argument('--list', action='store_true', help='List all reminders')

    args = parser.parse_args()


    message, notify_time = args.add if args.add else (None, None)
    reminder_type = args.type
    
    if message and notify_time:
        if reminder_type is not None:
            add_reminder(message, notify_time, reminder_type)
        else:
            add_reminder(message, notify_time)
    elif args.remove is not None:
        reminder_id = args.remove
        remove_reminder(reminder_id)
    elif args.list is not None:
        list_reminders()
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
