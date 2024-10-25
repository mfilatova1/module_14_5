import sqlite3

connection = sqlite3.connect("initiate.db")
cursor=connection.cursor()


def initiate_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products
                    (id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    price INTEGER NOT NULL)
                    ''')
    connection.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                        (id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        balance INTEGER NOT NULL)
                        ''')
    connection.commit()

initiate_db()

def add_users(username, email, age, balance=1000):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (username, email, age, "1000"))
    connection.commit()

def is_included(username):
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    for user in users:
        if user[1] == username:
            return True
    return False




cursor.execute('DELETE FROM Products')
for i in range(1, 5):
    cursor.execute("INSERT INTO Products (title, description, price) VALUES(?, ?, ?)", (f'Название {i}', f'описание {i}', f'Цена {i*100}',))
    connection.commit()

def get_all_products():
    cursor.execute("SELECT * FROM Products")
    return cursor.fetchall()

