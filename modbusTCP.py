import minimalmodbus
from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer
from time import sleep, asctime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_modbus():
    """Attempt to connect to the Modbus device until successful."""
    client = None
    while True:
        try:
            logging.info("Connecting to Modbus...")
            client = ModbusTcpClient("10.0.0.71", port=503, framer=ModbusRtuFramer)
            if client.connect():
                logging.info("Connected to Modbus!")
                return client
            else:
                logging.warning("Connection failed. Retrying...")
                sleep(3)
        except Exception as e:
            logging.error(f"Connection error: {e}. Retrying...")
            sleep(3)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    """Translate value from one range to another."""
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def read_modbus_data(client):
    """Read data from Modbus and display the results."""
    while True:
        try:
            result = client.read_input_registers(0, 7, unit=1)
            level_bst3_raw = result.registers[0]
            level_bst3 = translate(level_bst3_raw, 3998, 20005, 0, 9.260)
            level_bst3 = round(level_bst3, 3)

            logging.info(f"Raw Level BST3: {level_bst3_raw}, Scaled: {level_bst3}")
            sleep(5)

        except Exception as e:
            logging.error(f"Error reading Modbus data: {e}")
            sleep(1)

if __name__ == "__main__":
    client = None
    try:
        client = connect_modbus()
        read_modbus_data(client)
    finally:
        if client:
            client.close()
            logging.info("Modbus connection closed. Program terminated.")
