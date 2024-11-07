#!/usr/bin/env python3

import sqlite3
import subprocess
import time
import os
from datetime import datetime

home_dir = os.path.expanduser("~")
DB_FILE = os.path.join(home_dir, ".config", "notipy", "notipy.db")

def check_reminders():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE notify_time <= ?',(datetime.now(),))
        reminders = cursor.fetchall()
        for reminder in reminders:
            subprocess.run(['notify-send', f'notiPy reminder', f'{reminder[2]}: {reminder[1]}'])
            cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder[0],))
            conn.commit()

def main():
    while True:
        check_reminders()
        time.sleep(1)

if __name__ == "__main__":
    main()
