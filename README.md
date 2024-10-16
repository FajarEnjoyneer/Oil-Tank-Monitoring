# Sensor Monitoring Project

This project is designed to monitor and log sensor data from a Modbus device into a SQLite database and InfluxDB. It also provides an interface to push this data to a remote API.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [License](#license)

## Introduction

The Sensor Monitoring Project allows users to read sensor data from a Modbus device, store it in a SQLite database, and visualize or use it through an API. The data can also be sent to an InfluxDB for further analysis.

## Requirements

- Python 3.x
- Libraries:
  - `minimalmodbus`
  - `pymodbus`
  - `sqlite3`
  - `requests`
  - `influxdb`
- A running instance of InfluxDB
- A Modbus device for data acquisition

## Installation

Clone the repository:
   ```bash
   git clone https://github.com/FajarEnjoyneer/IoT-Sensor-Monitoring.git
   cd IoT-Sensor-Monitoring
   pip install minimalmodbus pymodbus influxdb requests sqlite3
   ```
## Usage
Create the database schema: Run createtable.py to create the SENSOR table in the SQLite database.
Read sensor data: Run modbusTCP.py to connect to the Modbus device and read sensor data. This script will also update the SQLite database.
Push sensor data to remote API: Run getSensor.py to push the sensor data to a specified API endpoint.

## File Descriptions
createTable.py: Creates the SQLite database and the SENSOR table.
modbusTCP.py: Connects to the Modbus device and reads sensor data, storing it in the SQLite database.
getSensor.py: Retrieves data from the SQLite database and pushes it to a remote API.

## License
1. Create a new file named `README.md` in your project directory. 
2. Copy and paste the above content into the `README.md` file.
3. Save the file.
Feel free to modify any sections to fit your specific project needs, such as adding examples, adjusting library requirements, or including additional instructions. If you need further assistance, let me know!
