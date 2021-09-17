from paho.mqtt import client as mqtt
import traceback
import ssl
import json
from confighelper import get_config
from postgresqladapter import insert_env_data, insert_pax_data

config = get_config()


def process_message(decoded_payload):
    try:
        payload_json = json.loads(decoded_payload)
        application_id = payload_json["end_device_ids"]["application_ids"]["application_id"]
        deveui = payload_json["end_device_ids"]["device_id"]
        timestamp = payload_json["received_at"]
        if application_id == "mitwelten-sensors":
            voltage = payload_json["uplink_message"]["decoded_payload"]["battery"]
            humidity = payload_json["uplink_message"]["decoded_payload"]["humidity"]
            temperature = payload_json["uplink_message"]["decoded_payload"]["temperature"]
            moisture = payload_json["uplink_message"]["decoded_payload"]["moisture"]
            insert_env_data(deveui, voltage, temperature, humidity, moisture, timestamp)
        if application_id == "mitwelten-pax":
            voltage = payload_json["uplink_message"]["decoded_payload"]["voltage"]
            pax = payload_json["uplink_message"]["decoded_payload"]["ble"]
            insert_pax_data(deveui, voltage, pax, timestamp)
    except Exception as e:
        print(e)
        traceback.print_exc()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(config["mqtt"]["subscribe_topic"], config["mqtt"]["qos"])


def on_message(client, userdata, msg):
    print(
        "Incomming mqtt message: Topic = ",
        msg.topic,
        " Payload size is ",
        len(msg.payload),
    )
    process_message(msg.payload.decode())


client = mqtt.Client()
client.username_pw_set(config["mqtt"]["username"], config["mqtt"]["password"])
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(
    certfile=None,
    keyfile=None,
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLSv1_2,
    ciphers=None,
)
client.tls_insecure_set(False)
client.connect(config["mqtt"]["host"], config["mqtt"]["port"], 60)

client.loop_forever()
