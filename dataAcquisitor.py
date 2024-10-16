import minimalmodbus
from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer
import sqlite3
from time import sleep
from random import uniform
from influxdb import InfluxDBClient
from datetime import datetime

# --- Configuration constants ---
MODBUS_IP = "10.0.0.71"
MODBUS_PORT = 503
SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 9600
DB_PATH = 'data.db'
INFLUX_CREDENTIALS = {'host': 'localhost', 'port': 8086, 'username': 'user', 'password': 'password', 'database': 'nameDB'}

# --- Setup InfluxDB client ---
clientInflux = InfluxDBClient(**INFLUX_CREDENTIALS)
clientInflux.switch_database(INFLUX_CREDENTIALS['database'])

# --- Initialize SQLite connection ---
def init_sqlite_connection(db_path):
    return sqlite3.connect(db_path)

# --- Modbus initialization ---
def init_modbus_client(ip, port):
    client = ModbusTcpClient(ip, port=port, framer=ModbusRtuFramer)
    while not client.connect():
        print("Reconnecting to Modbus...")
        sleep(5)
    print("Connected to Modbus!")
    return client

def init_modbus_device(port, slave_address):
    device = minimalmodbus.Instrument(port, slave_address)
    device.serial.baudrate = BAUDRATE
    device.serial.timeout = 0.1
    return device

# --- Data functions ---
def store_influx_data(data, bst1, bst2, bst3):
    data["time"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    data["fields"].update({"bst1": float(bst1), "bst2": float(bst2), "bst3": float(bst3)})
    clientInflux.write_points([data])

def update_sqlite_data(cursor, name, raw, value):
    cursor.execute("UPDATE SENSOR SET RAW = ?, VALUE = ? WHERE NAME = ?;", (raw, value, name))

def map_value(x, in_min, in_max, out_min, out_max):
    return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min, 3)

# --- Main loop ---
def main():
    client = init_modbus_client(MODBUS_IP, MODBUS_PORT)
    device_1 = init_modbus_device(SERIAL_PORT, 1)

    with init_sqlite_connection(DB_PATH) as connect:
        cursor = connect.cursor()

        while True:
            try:
                # Read data from Modbus device
                data_1 = device_1.read_registers(0, 8)
                level_bst1_raw, level_bst2_raw = data_1[0], data_1[7]

                # Convert raw data to actual values
                level_bst1 = map_value(level_bst1_raw, 3999, 20005, 0, 10.965)
                level_bst2 = map_value(level_bst2_raw, 3997, 20012, 0, 8.580)

                # Update SQLite with new sensor data
                update_sqlite_data(cursor, "Level_BST1", level_bst1_raw, level_bst1)
                update_sqlite_data(cursor, "Level_BST2", level_bst2_raw, level_bst2)
                connect.commit()

                # Read additional data from Modbus client
                value = client.read_input_registers(0, 7, 1)
                level_bst3_raw = value.registers[0]
                level_bst3 = map_value(level_bst3_raw, 3998, 20005, 0, 9.260)
                update_sqlite_data(cursor, "Level_BST3", level_bst3_raw, level_bst3)
                connect.commit()

                # Store data to InfluxDB
                store_influx_data(data_, level_bst1, level_bst2, level_bst3)

                # Wait before next read
                sleep(10)

            except Exception as error:
                print(f"Error: {error}")
                sleep(6)

if __name__ == "__main__":
    main()
