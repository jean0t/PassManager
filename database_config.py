import sqlite3 as sql
from pandas import DataFrame

def creating_db():
    try:
        conn = sql.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS login(hash)
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials(username, application, email, password)
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        print("Error creating database.")

def config_login(hash: str):
    conn = sql.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO TABLE login(hash) VALUES (?)
    """, (hash))
    conn.commit()
    cursor.close()
    conn.close()

def adding_db(username: str, application: str, email: str, password: str):
    conn = sql.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO TABLE credentials(username, application, email, password) VALUES (?, ?, ?, ?)
    """, (username, application, email, password))
    conn.commit()
    cursor.close()
    conn.close()
