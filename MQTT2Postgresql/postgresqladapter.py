import psycopg2
from confighelper import get_config

config = get_config()

connection_string = "dbname='" + config["postgresql"]["dbname"] + "'"
connection_string += " user='" + config["postgresql"]["username"] + "'"
connection_string += " host='" + config["postgresql"]["host"] + "'"
connection_string += " port=" + str(config["postgresql"]["port"])
connection_string += " password='" + config["postgresql"]["password"] + "'"

conn = psycopg2.connect(connection_string)
cur = conn.cursor()


def insert_env_data(deveui, voltage, temperature, humidity, moisture, timestamp):
    # check if humidity and temperature are 0:
    if (humidity == 0) and (temperature == 0):
        humidity = None
        temperature = None
    cur.execute(
        "INSERT INTO envsensordata (deveui, voltage,temperature, humidity, moisture,  time) VALUES(%s, %s, %s, %s, %s, %s)",
        (deveui, voltage, temperature, humidity, moisture, timestamp),
    )
    conn.commit()


def insert_pax_data(deveui, voltage, pax, timestamp):
    voltage = voltage / 1000  # mV to V
    cur.execute(
        "INSERT INTO paxsensordata (deveui, voltage , pax,  time) VALUES(%s, %s, %s, %s)",
        (deveui, voltage, pax, timestamp),
    )
    conn.commit()
