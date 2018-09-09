# IoT - MQTT using Python
### This is a Prototype model for IoT. This model is suitable for any IoT device that supports Python. The system can be integrated to send data from the device to the cloud using MQTT protocol, which is a lightweight protocol for machine to machine communication.<br/>On the other end, the system can be integrated for receiving the data over cloud for further analysis.<br/><br/>
 
 ### How the system works :<br/>
 >   The sender.py file is flashed into any micro controller like Arduino/Raspberry/Onion.<br/>
    The sender.py file is responsible for sending/publishing the data/values/parameter as a payload to cloud/broker.
    This data can collection of data fetched from the sensors. Broker is responsible for forwarding the same to all the
    subscribed listeners. The receiver.py is one of the subscribed listener. Once the receiver receives this
    payload/data, it can manage this data as per its needs like for just storing into data or for further analysis and
    machine learning and many more purposes.<br/><br/>

### FILE LIST :-
>    IoT1 
      |- templates
           >- index.html
      |- dbSetup.py
      |- README.md
      |- mydb.db
      |- receiver.py
      |- sender.py
 
### Dependencies in receiving server :-<br/>
>    python v3<br/>
    flask<br/>
    flask-mqtt<br/>
    flask-socketio<br/>
    eventlet<br/><br/>

### Dependencies in Sending equipment :-<br/>
>    python v3<br/>
    paho-mqtt<br/><br/>

> Suitable Public Brokers for MQTT :-<br/>
    1. Eclipse - iot.eclipse.org<br/>
    2. Mosquitto - test.mosquitto.org<br/>
    3. Hive - broker.hivemq.com<br/><br/>

> You can also create your own private Broker for MQTT by using the software provided by hive at https://www.hivemq.com/downloads/
<br/><br/><br/> 

### The project is still under its initial stages of development and we welcome any kind of suggestions or improvements. 
Project being improved by me and [@anantkaushik](https://github.com/anantkaushik)
