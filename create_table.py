import sqlite3

connection = sqlite3.connect('data/data.db')
cursor = connection.cursor()

# INTEGER -> auto-incrementing columns
query_create = "CREATE TABLE IF NOT EXISTS users VALUES (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(query_create)

query_create_2 = "CREATE TABLE IF NOT EXISTS items VALUES (items text PRIMARY KEY, price real)"
cursor.execute(query_create_2)

connection.commit()
connection.close()
