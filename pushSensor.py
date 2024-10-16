import sqlite3
from time import sleep, asctime
import requests
import logging
import certifi

Log_Format = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(    filename="/home/crocodic-raspi/Project/SJMS/Log/pushSensor.log",
                        filemode="a",
                        format= Log_Format,
                        level=logging.DEBUG )
logger = logging.getLogger()

connect = sqlite3.connect('/home/crocodic-raspi/Project/SJMS/data.db')


cursor = connect.cursor()

def push(data):
    url = "https://thingsboard.cloud/api/device/all"
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
            "Accept": "/",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest"
           }
    response = requests.post(url=url, headers=headers, json=data, verify=certifi.where())

while True:
    try:
        sensor = []
        print(asctime())
        data=cursor.execute('''SELECT * FROM SENSOR''')
        for row in data:
            print(row)
            sensor.append(row)

        # Station 1
        level_bst1 = sensor[0][3]
        level_bst2 = sensor[1][3]
        level_bst3 = sensor[2][3]

        data = {
            'MT1':{
                'level' : level_bst1
            },
            'MT2':{
                'level' : level_bst2
            },
            'MT3':{
                'level' : level_bst3
            }
        }
        push(data)
        sensor.clear()
        sleep(60)

    except Exception as error:
        print(error)
