"""
This file, along with the HTML page, needs to be uploaded on cloud service which supports web sockets like AWS.

How this file works :
    This file first subscribes to a topic when the HTML page is opened. Then it will receive any message with same topic
    over the MQTT broker. Once the message is received, this file stored the value into the SQLite3 Database. Every time
    the page is reloaded, the displayed data is refreshed(again fetched from the database).

Required python libraries(dependencies): (use pip install)
    python v3
    flask
    flask-mqtt
    flask-socketio
    eventlet

References :
    MQTT - https://mqtt.org/tag/paho    (lightweight connectivity protocol for M2M communication)
    flask - http://flask.pocoo.org/     (Micro web framework written in python)
    flask-socket - https://flask-socketio.readthedocs.io/en/latest/     (web sockets compatible with flask)
    SQLite3 - https://www.sqlite.org/index.html     (lightweight relational database)
    custom broker - https://www.hivemq.com/downloads/   (Creating your own custom broker)
"""

# this is a test program which receives the the timestamp when the light is turned on or off and stores it into the database

from flask import Flask, render_template, redirect
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
import eventlet, sqlite3 as sql,json

# initialising flask
app = Flask(__name__, static_url_path='')
eventlet.monkey_patch()

# configuring app for required MQTT parameters
app.secret_key = 'anantranajoykey'      #keep it secret
app.config['SECRET'] = '121202'         #keep it secret
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'iot.eclipse.org'       # suitable free brokers - iot.eclipse.org / test.mosquitto.org / broker.hivemq.com
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'Ranajoy'
app.config['MQTT_PASSWORD'] = '123456'
app.config['MQTT_KEEPALIVE'] = 10
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'sigmaway/akrd/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
app.config['MQTT_LAST_WILL_QOS'] = 2


# initialising MQTT
mqtt = Mqtt(app)

# initialising socket
socketio = SocketIO(app)

# Function for storing data into database table
def toDatabase(data):
    try:
        conn = sql.connect('mydb.db')       # connecting to database
        cur = conn.cursor()                 # setting the cursor
        # SQL query for insertion into table
        cur.execute("INSERT INTO dataTable (new_state, timestamps) VALUES ('%s','%f')"%(data['state'],data['timestamp']))
        conn.commit()   # saving the changes
        cur.close()     # closing cursor
        conn.close()    # closing the connection
        # print("Successfully stored into Database")
    except Exception as e:
        print("An error occurred\n"
              "Error : ", e)

# function for fetching data from database table
def al():
    con = sql.connect("mydb.db")    # creating connection with database
    con.row_factory = sql.Row
    cur = con.cursor()              # setting the cursor
    cur.execute("select * from dataTable")  # SQL query for fetching all of the data from the table
    rows = cur.fetchall();          # fetching the data and storing it into a variable
    cur.close()                     # closing the cursor
    con.close()                     # closing the connection
    return rows

# routing home page (HTML page)
@app.route('/')
def index():
    handle_subscribe()      # Function Call to subscribe to the topic
    rows = al()             # function call to fetch values from the Table (Database)
    return render_template('index.html', rows = rows)   # rendering the HTML page and passing the fetched values

# function to subscribe to the topic
@socketio.on('subscribe')
def handle_subscribe():
    topic = 'sigmaway/akrd/db1'     # topic name, must be same as the topic name of publisher
    qos = 0
    mqtt.subscribe(topic, qos)      # MQTT function call to subscribe to the topic
    # print("*********Susbscibed !! *************")

# function to print the log data
@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

# function to receive the message from the broker
@mqtt.on_message()      # triggered when any message is sent from publisher (prior subscription is must)
def handle_mqtt_message(client, userdata, message):
    payload=message.payload.decode()        # decoding the message
    # print("***** message received = \n", payload, "*****")
    if payload != "":                       # if payload is not empty
        json_acceptable_string = payload.replace("'", "\"")
        data = json.loads(json_acceptable_string)       # converting data into json format
        toDatabase(data)            # function call for storing data into database

# function to clear the data in table (triggered on button click from the HTML page)
@app.route('/clearData')
def clearData():
    try:
        conn = sql.connect('mydb.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM dataTable")
        cur.execute("DELETE FROM sqlite_sequence WHERE name = 'dataTable';")    # resetting the autoincrement field
        conn.commit()
        cur.close()
        conn.close()
        # print("Database Cleared")
    except Exception as e:
        print("An error occurred\n"
              "Error : ", e)
    finally:
        return redirect('/')        # return Home Page

# running the main thread
if __name__ == '__main__':
    # running the socket at localhost at port 5000
    # set debug = False before deploying it for commercial use
    socketio.run(app, host='127.0.0.1', port=5000, use_reloader=True, debug=True)
