#!/usr/bin/python

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import Adafruit_DHT
import time
import sys
import datetime
from Adafruit_IO import *
#from influxdb import InfluxDBClient

verbose = 1

def connected(client):
	print('Connected to Adafruit IO!')
    
def clean_DH(humid, temp):    
	if temp < 80 and temp > -40:
		temp = temp * 1.8 + 32
        	temp = round(temp, 1)
	else:
 		temp = None
    
	if humid < 100 and humid > 1:
        	humid = round(humid, 1)
    	else:
        	humid = None
        
	
	return humid, temp

# def write_to_influx(json):
#    """Writes values to Influx database"""
#    host='localhost'
#    port = 8086
#    user = 'root'
#    password = 'root'
#    dbname = 'OfficeTemp'

#    client = InfluxDBClient(host, port, user, password, dbname)

#    client.create_database(dbname)

#    client.write_points(json)
    

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22
aio = Client('4551326023d44215bc73c6367ad1b8f0')
mqtt = MQTTClient('tlbradshaw','4551326023d44215bc73c6367ad1b8f0')

connection_type = 'mqtt_pub'

mqtt.on_connect = connected

# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
# pin = 'P8_11'

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
pin = 17

try:
#	print('Attempting to connect')
	mqtt.connect()
	mqtt.loop_background()
except:
#	print('Error Connecting')
	connection_type = 'api_pub'
	pass	


# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).

while True:
     print('Getting values...')
     humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
     print('Values received.')

     #temperature = temperature * 1.8 + 32
     #temperature = round(temperature, 1)
     #humidity = round(humidity, 1)
#     print('Cleaning values...')
     humidity, temperature = clean_DH(humidity, temperature)
#     print('Values cleaned.')

     # Note that sometimes you won't get a reading and
     # the results will be null (because Linux can't
     # guarantee the timing of calls to read the sensor).
     # If this happens try again!
     if humidity is not None and temperature is not None:
	if connection_type == 'mqtt_pub':
             try:
                mqtt.publish('home-temperature', te6mperature)
                mqtt.publish('home-humidity', humidity)
		if verbose:
			print('temp: ' +  temperature)
			print('humidity: ' +  humidity)
             except:
		if verbose:
			print('MQTT Publish Failed.')
                pass           
        else:
            try:
		aio.send('office-temperature',temperature)
		aio.send('office-humidity', humidity)
		if verbose:
			print('temp: ' +  temperature)
			print('humidity: ' +  humidity)
            except:
		if verbose:
			print('AIO Publish Failed.')
		pass
        json_body = [
             {
                "measurement": "office-temperature",
                "tags": {
                    "location": "office"
                },
                "fields": {
                    "Temperature": temperature,
                    "Humidity": humidity
                }
             }
        ]         
#        try:
#           write_to_influx(json_body)
#        except:
#           pass

     time.sleep(300)
