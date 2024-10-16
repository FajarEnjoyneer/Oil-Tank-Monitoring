import sqlite3
from time import sleep, asctime
import requests

DB_PATH = 'data.db'
API_URL = "https://api/device/all"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
    "Accept": "/",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest"
}

def push(data):
    try:
        response = requests.post(url=API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error pushing data: {e}")

def get_sensor_data(cursor):
    cursor.execute('''SELECT * FROM SENSOR''')
    return cursor.fetchall()

def main():
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    while True:
        try:
            print(asctime())
            sensors = get_sensor_data(cursor)
            if len(sensors) >= 3:
                level_bst1 = sensors[0][3]
                level_bst2 = sensors[1][3]
                level_bst3 = sensors[2][3]
                data = {
                    'MT1': {'level': level_bst1},
                    'MT2': {'level': level_bst2},
                    'MT3': {'level': level_bst3}
                }
                push(data)
            else:
                print("Not enough sensors available.")
            sleep(1)
        except Exception as error:
            print(f"Error retrieving sensor data: {error}")
            sleep(5)
    connect.close()

if __name__ == "__main__":
    main()
