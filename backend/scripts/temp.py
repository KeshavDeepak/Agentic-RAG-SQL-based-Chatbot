import sqlite3

conn = sqlite3.connect("backend/data/adventureworks.sqlite")
cursor = conn.cursor()

cursor.execute("pragma table_info('Sales.Store')")
print(cursor.fetchall())

conn.close()