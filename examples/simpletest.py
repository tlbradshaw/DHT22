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

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22
aio = Client('4551326023d44215bc73c6367ad1b8f0')

# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
# pin = 'P8_11'

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
pin = 17


# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).

while True:

     humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
     temperature = temperature * 1.8 + 32
     temperature = round(temperature, 1)
     humidity = round(humidity, 1)

     # Note that sometimes you won't get a reading and
     # the results will be null (because Linux can't
     # guarantee the timing of calls to read the sensor).
     # If this happens try again!
     if humidity is not None and temperature is not None:
#	 sttime = datetime.datetime.now().strftime('%x_%H:%M:%S ')
#	 with open('templog.log','a') as logfile:
#	      logfile.write(sttime + 'Temp={0:0.1f}*F Humidity={1:0.1f}%'.format(temperature, humidity) + '\n')
	 try:
         	aio.send('office-temperature',temperature)
         	aio.send('office-humidity', humidity)
	 except:
#		with open('temperror.log','a') as errorlog:
#			errorlog.write(sttime + ' Failure to send sensor data to Adafruit' + '\n')
		#print(sttime, sys.exc_info()[0])
	 	pass
        # print(sttime + 'Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format(temperature, humidity))
     #else:
         # print('Failed to get reading. Try again!')

	
     time.sleep(300)

