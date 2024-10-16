import sqlite3

connect = sqlite3.connect('data.db')
cursor = connect.cursor()
print("Sensor Table:")
data = cursor.execute('''SELECT * FROM SENSOR''')
for row in data:
    print(row)
connect.close()
