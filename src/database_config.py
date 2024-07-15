import sqlite3 as sql
from pandas import DataFrame
from encrypting import hash256
from secrets import compare_digest
from hashlib import md5
from cryptography.fernet import Fernet
from random_password import clipboard_copy

def creating_db():
    try:
        conn = sql.connect(".database.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS login(hash)
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials(id, username, application, email, password)
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except:
        print("Error creating database.")

def config_login(key: bytes):
    hash = hash256(key)
    conn = sql.connect(".database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO login VALUES (?)
    """, (hash,))
    conn.commit()
    cursor.close()
    conn.close()

def adding_db(username: str, application: str, email: str, password: str):
    id = md5(application.encode("utf-8")).hexdigest()
    conn = sql.connect(".database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO credentials VALUES (?, ?, ?, ?, ?)
    """, (id[:5], username, application, email, password))
    conn.commit()
    cursor.close()
    conn.close()

def deleting_db(username: str, application: str):
    id = md5(application.encode("utf-8")).hexdigest()
    conn = sql.connect(".database.db")
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM credentials WHERE id = ? AND username = ? 
    """, (id[:5], username))
    conn.commit()
    cursor.close()
    conn.close()

def showing_db():
    conn = sql.connect(".database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM credentials 
    """)
    data = cursor.fetchall()
    indexes = [''] * len(data)
    df = DataFrame(data= data, index=indexes,columns=("id", "username", "application", "email", "password"))
    df['password'] = '[hidden]'
    print(df)
    conn.commit()
    cursor.close()
    conn.close()

def copying_passwd_db(id: str, username: str) -> str:
    conn = sql.connect(".database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM credentials 
    """)
    data = cursor.fetchall()
    for element in data:
        if (id == element[0] and username == element[1]):
            clipboard_copy(element[4])
        
    conn.commit()
    cursor.close()
    conn.close()

def check_login(key: bytes) -> bool:
    conn = sql.connect(".database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT hash from login
    """)
    hash = cursor.fetchone()[0]
    print(hash, type(hash))
    hash_key = hash256(key)
    result = compare_digest(str(hash), hash_key)
    cursor.close()
    conn.close()

    return result

def encrypting_db(key: bytes) -> None:
    f = Fernet(key= key)
    with open(".database.db", "rb") as file:
        contents = file.read()

    contents = f.encrypt(contents)

    with open(".database.db", "wb") as file:
        file.write(contents)

def decrypting_db(key: bytes) -> None:
    with open(".database.db", "rb") as file2:
        contents = file2.read()

    contents = Fernet(key= key).decrypt(contents)

    with open(".database.db", "wb") as file:
        file.write(contents)