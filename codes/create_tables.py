import sqlite3

connection = sqlite3.connect("database/data.db")
cursor = connection.cursor()

create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_users_table)

connection.commit()
connection.close()
