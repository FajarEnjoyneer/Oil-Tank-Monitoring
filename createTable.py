import sqlite3
DB_PATH = 'data.db'

# --- Function to initialize the database ---
def initialize_database(db_path):
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute("DROP TABLE IF EXISTS SENSOR")
    cursor.execute("""CREATE TABLE SENSOR (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME VARCHAR(255),
                        RAW INTEGER,
                        VALUE INTEGER,
                        SESSION VARCHAR(255)
                     );""")
    initial_sensors = [
        ("Level_BST1", 0, 0),
        ("Level_BST2", 0, 0),
        ("Level_BST3", 0, 0),
    ]
    cursor.executemany('''INSERT INTO SENSOR(NAME, RAW, VALUE) VALUES (?, ?, ?)''', initial_sensors)
    connect.commit()
    return connect, cursor
def display_sensor_data(cursor):
    print("Sensor Table: ")
    data = cursor.execute('''SELECT * FROM SENSOR''')
    for row in data:
        print(row)

def main():
    connect, cursor = initialize_database(DB_PATH)
    display_sensor_data(cursor)
    connect.close()

if __name__ == "__main__":
    main()
