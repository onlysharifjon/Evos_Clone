import sqlite3

connect = sqlite3.connect('evos_database.db')
cursor = connect.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, phone INTEGER, longitude TEXT NULL, latitude TEXT NULL)")


async def add_user(user_id,tel_number):
    cursor.execute('INSERT INTO users(user_id, phone) VALUES (?, ?)', (int(user_id), tel_number))


    connect.commit()

async def check_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?",(user_id,))
    row = cursor.fetchone()
    if row is None:
        return True
    else:
        return False