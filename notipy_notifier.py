#!/usr/bin/env python3

import sqlite3
import subprocess
import time
import os
from datetime import datetime, timedelta

home_dir = os.path.expanduser("~")
DB_FILE = os.path.join(home_dir, ".config", "notipy", "notipy.db")

def check_reminders():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE notify_time <= ?', (datetime.now(),))
        reminders = cursor.fetchall()
        
        for reminder in reminders:
            reminder_id = reminder[0]
            message = reminder[1]
            notify_time = reminder[2]
            add_time = reminder[3]
            reminder_type = reminder[4]
            
            # Send notification
            subprocess.run([
                'notify-send',
                "notiPy Reminder",
                message,
                '--icon=dialog-information',  
                '--urgency=normal'
            ])

            if reminder_type == 'single':
                cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
            
            elif reminder_type == 'daily':
                next_notify = datetime.strptime(notify_time, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
                cursor.execute('UPDATE reminders SET notify_time = ? WHERE id = ?', (next_notify, reminder_id))
            
            elif reminder_type == 'weekly':
                next_notify = datetime.strptime(notify_time, '%Y-%m-%d %H:%M:%S') + timedelta(weeks=1)
                print(next_notify)
                cursor.execute('UPDATE reminders SET notify_time = ? WHERE id = ?', (next_notify, reminder_id))
            
            conn.commit()

def main():
    while True:
        check_reminders()
        time.sleep(1)

if __name__ == "__main__":
    main()

