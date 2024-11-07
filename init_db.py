#!/usr/bin/bash

import sqlite3
import os

home_dir = os.path.expanduser('~')
DB_FILE = os.path.join(home_dir, '.config', 'notipy', 'notipy.db')

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

    # Initialize the database
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                message TEXT NOT NULL,
                notify_time TIMESTAMP NOT NULL,
                add_time TIMESTAMP NOT NULL,
                reminder_type TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

