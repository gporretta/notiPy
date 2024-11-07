#!/usr/bin/env python3

import sqlite3
import time
import argparse
import os
from datetime import datetime

home_dir = os.path.expanduser("~")
DB_FILE = os.path.join(home_dir, ".config", "notipy", "notipy.db")

def add_reminder(message, notify_time):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reminders (message, notify_time, add_time, reminder_type) VALUES ( ?, ?, ?, ?)
        ''', (message, notify_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'single'))
        conn.commit()
    print(f"Added reminder: '{message}' for {notify_time}")

def remove_reminder(reminder_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id))
        conn.commit()
    print(f"Removed reminder: ID = {reminder_id}")

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
    parser.add_argument('--add', nargs=2, help='Add a reminder: message time')
    parser.add_argument('--remove', type=int, help='Remove a reminder by ID')
    parser.add_argument('--list', action='store_true', help='List all reminders')

    args = parser.parse_args()

    if args.add:
        message, time_str = args.add
        notify_time = time_str
        add_reminder(message, notify_time)
    elif args.remove is not None:
        remove_reminder(args.remove)
    elif args.list is not None:
        list_reminders()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
