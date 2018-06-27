# -*- coding: utf-8 -*-
"""
This file is responsible for collecting humidity and temperature from DHT-11 sensor at regular intervals and send the same 
to MQTT broker in json format.

How this file works :
    sender.py is flashed into the micro controller along with the required code for fetching data from necessary sensors.
    This file then publishes(sends) the data to the broker. Broker can be a public broker like iot.eclipse.org or
    test.mosquitto.org or broker.hivemq.com. Or it can be a custom server that supports MQTT protocols.

Required libraries (dependencies):
    python v3
    paho-mqtt
"""
# currently this test file sends a toggle value of on/off along with a timestamp. This can be changed with your sensor values

import subprocess
import paho.mqtt.client as mqtt  # import the client1
import time, json

# broker_address="192.168.1.184"
broker_address = "iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("akrdClient")  # create new instance
try:
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    client.loop_start()  # start the loop
    i=0
    while i < 25:
        pinNumber = 0
        sensorModel = 'DHT11'
        proc = subprocess.Popen(['dht-sensor ' + str(pinNumber) + ' ' + sensorModel], stdout=subprocess.PIPE,
                                shell=True)
        (out, err) = proc.communicate()
        sensor_data = out.split('\n')
        humidity = sensor_data[0]
        temperature = sensor_data[1]
        # print "Humidity:"
        print
        str(humidity) + "%"
        # print "Temperature:"
        print
        str(temperature) + "°C\n"
        data = json.dumps({'humidity': humidity, 'temperature': temperature,
                           'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                               time.time()))})  # json is a recommended data format

        print("Publishing message to topic", "sigmaway/akrd/db1")
        client.publish("sigmaway/akrd/db1"
                       "", data)
        print('data = ', data, i + 1)
        time.sleep(3.5)  # wait
        i += 1
except Exception as e:
    print("Error occured : ", e)

client.loop_stop()  # stop the loop
