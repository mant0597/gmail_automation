import sqlite3

conn = sqlite3.connect('emails.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM emails")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
