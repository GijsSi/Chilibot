import sqlite3

conn = sqlite3.connect('chilibot.sqlite')

# Create a cursor object using the cursor method
cursor = conn.cursor()

# Create table with specific columns for each sensor value
cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_values (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    average_distance REAL,
    soil_moisture REAL,
    air_temperature REAL,
    air_humidity REAL,
    water_level REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS command_log (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    command TEXT,
    parameters TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

def save_sensor_values(average_distance=None, soil_moisture=None, air_temperature=None, air_humidity=None, water_level=None):
    conn = sqlite3.connect('chilibot.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO sensor_values (average_distance, soil_moisture, air_temperature, air_humidity, water_level) 
           VALUES (?, ?, ?, ?, ?)''', 
        (average_distance, soil_moisture, air_temperature, air_humidity, water_level)
    )
    conn.commit()
    conn.close()

def log_command(command, parameters=""):
    conn = sqlite3.connect('chilibot.sqlite')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO command_log (command, parameters) VALUES (?, ?)", (command, parameters))
    conn.commit()
    conn.close()

