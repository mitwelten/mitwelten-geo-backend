# MQTT2Postgresql

An adapter to write MQTT messages from TTN to Postgresql

## Requirements

```sh
pip3 install paho-mqtt
pip3 install psycopg2
```



## Configuration

The configuration is done in a config file (see [sampleconfiguration.conf](sampleconfiguration.conf))

Parameter|Description
-|-
mqtt.host|mqtt broker url
mqtt.port|mqtt broker port
mqtt.username|mqtt username
mqtt.password|mqtt password
mqtt.subscribe_topic|topic to subscribe to
mqtt.qos|subscribe qos
postgresql.host|postgresql host
postgresql.port|postgresql port
postgresql.dbname|name of the database
postgresql.username|postgresql username
postgresql.password|postgresql password

## Run it

```sh
python3 MQTT2Postgresql.py -i path_to_the_configfile
```

Or use the [service script](mqtt2psql_sensors.service)


