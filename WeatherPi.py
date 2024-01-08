# Remixed from source code found at https://raspberrypiandstuff.wordpress.com/2017/08/07/uploading-aprscwop-weather-data/
# Program to send weather data from DHT11 to APRS-IS network

#!/usr/bin/env python

import sys
from datetime import datetime
from socket import *
import Adafruit_DHT

serverHost = 'rotate.aprs.net' # Use an APRS server for your continent
serverPort = 14580
address = 'YOUR_CALL>APRS,TCPIP*:' # Replace "YOUR_CALL" with your callsign and ssid (Ex. N0CALL-13)
position = 'DDMM.SSN/DDDMM.SSW_' #Replace with your lat/lon in Degrees, Minutes, Seconds

def send_packet():
    # Get temperature and humidity values from DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, GPIO_PIN)
    
    # Convert temperature to Fahrenheit
    fahrenheit = 9.0/5.0 * temperature + 32

    # Set wind-related variables to None
    wind_degrees = None
    wind_mph = None
    wind_gust_mph = None
    precip_1hr_in = None
    precip_today_in = None

    # Prepare the data, which will be sent
    wx_data = make_aprs_wx(wind_degrees, wind_mph, wind_gust_mph, fahrenheit, precip_1hr_in, None, None, humidity, None)

    # Use UTC
    utc_datetime = datetime.utcnow()

    # Create socket and connect to server
    sSock = socket(AF_INET, SOCK_STREAM)
    sSock.connect((serverHost, serverPort))
    # Log on
    sSock.send(b'user YOUR_CALL pass YOUR_PASS vers Python\n') # Replace YOUR_CALL with your callsign, and replace YOUR_PASS with your APRS passcode.

    # Send packet
    packet = (address + '@' + utc_datetime.strftime("%d%H%M") + 'z' + position + wx_data + 'Raspberry Pi DHT11 Weather Station\n').encode() # Station Comment. You may change Raspberry Pi DHT11 Weather Station to anything you want.
    sSock.send(packet)
    #Server Response
    response = sSock.recv(1024)

    # Close socket, must be closed to avoid buffer overflow
    sSock.shutdown(0)
    sSock.close()

def make_aprs_wx(wind_dir=None, wind_speed=None, wind_gust=None, temperature=None, rain_last_hr=None, rain_last_24_hrs=None, rain_since_midnight=None, humidity=None, pressure=None):
    # Assemble the weather data of the APRS packet
    def str_or_dots(number, length):
        if number is None:
            return '.' * length
        else:
            format_type = {
                'int': 'd',
                'float': '.0f',
            }[type(number).__name__]
            return ''.join(('%0', str(length), format_type)) % number

    return '%s/%sg%st%sr%sp%sP%sh%sb%s' % (
        str_or_dots(wind_dir, 3),
        str_or_dots(wind_speed, 3),
        str_or_dots(wind_gust, 3),
        str_or_dots(temperature, 3),
        str_or_dots(rain_last_hr, 3),
        str_or_dots(rain_last_24_hrs, 3),
        str_or_dots(rain_since_midnight, 3),
        str_or_dots(humidity, 2),
        str_or_dots(pressure, 5),
    )

try:
    GPIO_PIN = 6  # Set the GPIO PIN your DHT11 is connected to
    send_packet()
except Exception as e:
    print("Error:", e)
    sys.exit(-1)
