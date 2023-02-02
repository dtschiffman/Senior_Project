############################
# MQQT Client Subscription #
############################
#
# This script will listen for the "test/jpg" and "test/text"
# messages. It is assumed that the message payload for "test/jpg"
# is binary where "test/text" is text. 
#
import time
import paho.mqtt.client as mqtt

# change this to the ip of the broker
mqtt_server = "10.9.6.152"
#mqtt_server = "192.168.1.1"

# anonymous client. This option needs to be enabled on the broker during setup
client_id = "Dallin"

jpg_topic="test/jpg"
# Destination filename for the received jpeg file
jpg_filename="test.jpg"
text_topic="test"
# Destination filename for the received txt file
text_filename="test.txt"

def on_message(client, userdata, message):
    print("Receiving Message")
    print(message.topic)
    if (message.topic == jpg_topic):
        print("Saving file: "+jpg_filename)
        f=open(jpg_filename, "wb") # 'w' for 'write', 'b' for 'write as binary,>
        f.write(message.payload)
        f.close()

    if (message.topic == text_topic):
        print("Saving file: "+text_filename)
        txt = str(message.payload, 'UTF-8') # Encode the string with utf-8
        print(txt)
        f=open(text_filename, "w") # 'w' for 'write' defaults to uft-8, not binary
        f.write(txt)
        f.close()

def mqtt_connect():
    client = mqtt.Client(client_id)
    client.connect(mqtt_server)
    client.subscribe(text_topic)
    client.subscribe(jpg_topic)
    client.on_message = on_message
    print("Waiting\n")
    client.loop_forever() # Keeps waiting for published files, does not exit.

# Entry point of the script
mqtt_connect()
