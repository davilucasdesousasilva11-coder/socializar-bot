import sqlite3

def connect():
    conn = sqlite3.connect("database.socializar.db")
    return conn

def setup():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER PRIMARY KEY, 
                   coins INTEGER DEFAULT 0,
                   reputation INTEGER DEFAULT 0,
                   level INTEGER DEFAULT 1,
                   xp INTEGER DEFAULT 0
                   )
                   """)
    
    conn.commit()
    conn.close()