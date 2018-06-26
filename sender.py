"""

How this file works :
    sender.py is flashed into the micro controller along with the required code for fetching data from necessary sensors.
    This file then publishes(sends) the data to the broker. Broker can be a public broker like iot.eclipse.org or
    test.mosquitto.org or broker.hivemq.com. Or it can be a custom server that supports MQTT protocols.

Required libraries (dependencies):
    python v3
    paho-mqtt
"""
# currently this test file sends a toggle value of on/off along with a timestamp. This can be changed with your sensor values

import paho.mqtt.client as mqtt #import the client1
import time,json


# broker_address="192.168.1.184"
broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("akrdClient") # create new instance
try:
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    client.loop_start()             # start the loop

    # test toggle program sends value only 10 times. This can be changed to work infinite times or upto desired limit
    val = 'ON'
    i=0
    while i<10:
        if val == 'ON':
            val = 'OFF'
        else:
            val ='ON'
        data = json.dumps({'state':val,'timestamp':time.time()})        # json is a recommended data format
        print("Publishing message to topic","sigmaway/akrd/db1")
        client.publish("sigmaway/akrd/db1"
                       "",data)
        print('data = ',data,i+1)
        time.sleep(4) # wait
        i+=1
except Exception as e:
    print("Error occured : ", e)

client.loop_stop() #stop the loop
