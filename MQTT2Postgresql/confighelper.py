import configparser
import sys

if len(sys.argv) == 1:
    print("please provide a config file")
    exit()
if len(sys.argv) == 2:
    config_filename = sys.argv[1]
if len(sys.argv) == 3:
    config_filename = sys.argv[2]

config = {
    "mqtt": {
        "host": None,
        "port": 8883,
        "username": None,
        "password": None,
        "qos": 1,
        "subscribe_topic": None,
    },
    "postgresql": {
        "host": None,
        "port": 5432,
        "dbname": None,
        "username": None,
        "password": None,
    },
}


def read_configuration(conf):
    config = configparser.ConfigParser()
    # Read required Parameters
    try:
        config.read(config_filename)
        conf["mqtt"]["host"] = config["mqtt"]["host"]
        conf["mqtt"]["port"] = int(config["mqtt"]["port"])
        conf["mqtt"]["username"] = config["mqtt"]["username"]
        conf["mqtt"]["password"] = config["mqtt"]["password"]
        conf["mqtt"]["qos"] = int(config["mqtt"]["qos"])
        conf["mqtt"]["subscribe_topic"] = config["mqtt"]["subscribe_topic"]

        conf["postgresql"]["host"] = config["postgresql"]["host"]
        conf["postgresql"]["port"] = int(config["postgresql"]["port"])
        conf["postgresql"]["username"] = config["postgresql"]["username"]
        conf["postgresql"]["password"] = config["postgresql"]["password"]
        conf["postgresql"]["dbname"] = config["postgresql"]["dbname"]
    except KeyError as e:
        print(
            "[E] Missing Parameter in "
            + str(config_filename)
            + " ["
            + str(e.args[0])
            + "]"
        )
        print("Check config File and Restart.")
        exit(1)
    return conf


config = read_configuration(config)


def get_config():
    return config
