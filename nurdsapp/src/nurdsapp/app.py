"""
Smartphone app for the New Universal Recreation Device System
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import time
import paho.mqtt.client as mqtt
from threading import Thread
############################
# MQQT Client Subscription #
############################
#
# This script will listen for the "test/jpg" and "test/text"
# messages. It is assumed that the message payload for "test/jpg"
# is binary where "test/text" is text. 
#


class NURDSApp(toga.App):
    def mqtt_connect(self):
        client = mqtt.Client(self.client_id)
        client.connect(self.mqtt_server)
        client.subscribe(self.text_topic)
        client.subscribe(self.jpg_topic)
        client.on_message = self.on_message
        print("Waiting\n")
        client.loop_start()
        self.client = client
        client.publish(topic="test",payload="Message")
        #client.loop_forever() # Keeps waiting for published files, does not exit.       
    def publish(topic, message):
        self.client.publish(topic=topic, payload=message)
        
    def on_message(self, client, userdata, message):
        print("Receiving Message")
        print(message.topic)
        if (message.topic == self.jpg_topic):
            print("Saving file: "+self.jpg_filename)
            f=open(self.jpg_filename, "wb") # 'w' for 'write', 'b' for 'write as binary,>
            f.write(message.payload)
            f.close()

        if (message.topic == self.text_topic):
            print("Saving file: "+self.text_filename)
            txt = str(message.payload, 'UTF-8') # Encode the string with utf-8
            print(txt)
            f=open(self.text_filename, "w") # 'w' for 'write' defaults to uft-8, not binary
            f.write(txt)
            f.close()
            self.mess= txt
            
            #self.say_hello()

    def startup(self):
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        # change this to the ip of the broker
        self.mqtt_server = "144.39.210.225"
        #mqtt_server = "192.168.1.1"

        # anonymous client. This option needs to be enabled on the broker during setup
        self.client_id = "Dallin"

        self.jpg_topic="test/jpg"
        # Destination filename for the received jpeg file
        self.jpg_filename="test.jpg"
        self.text_topic="test"
        # Destination filename for the received txt file
        self.text_filename="test.txt"

        

        self.name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(self.name_label)
        name_box.add(self.name_input)



        self.main_box.add(name_box)
        
        self.mqtt_connect()
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()
        

    def say_hello(self):
        self.label(toga.Label(self.mess,style=Pack(padding=(0,5))))


def main():
    return NURDSApp()









