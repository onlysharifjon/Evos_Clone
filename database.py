import sqlite3

connect = sqlite3.connect('evos_database.db')
cursor = connect.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, phone INTEGER, longitude TEXT NULL, latitude TEXT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS products(img TEXT,name TEXT,price INTEGER,category TEXT)")
connect.commit()

async def add_user(user_id, tel_number):
    cursor.execute('INSERT INTO users(user_id, phone) VALUES (?, ?)', (int(user_id), tel_number))

    connect.commit()


async def check_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        return True
    else:
        return False


async def update_location(user_id, longitude, latitude):
    cursor.execute("UPDATE users SET longitude = ?, latitude = ? WHERE user_id = ?",
                   (longitude, latitude, user_id))
    connect.commit()



async def part_menyu(category):
    cursor.execute("CREATE TABLE IF NOT EXISTS products(img TEXT,name TEXT,price INTEGER,category TEXT)")
    connect.commit()


async def add_product(img, name, price, category):
    cursor.execute('INSERT INTO products VALUES(?,?,?,?)',(img,name,price,category))

    connect.commit()


cursor.execute('CREATE TABLE IF NOT EXISTS counts (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE,count INTEGER)')

async def check_count(user_id):
    print(True)
    a = cursor.execute('SELECT * FROM counts WHERE user_id = ?', (user_id,)).fetchall()
    print(a)
    d = []
    if a == d:
        cursor.execute('INSERT INTO counts(user_id, count) VALUES(?,?)', (user_id,0))
        connect.commit()
    else:
        cursor.execute('UPDATE counts SET count = 0 WHERE user_id = ?', (user_id,))
        connect.commit()
