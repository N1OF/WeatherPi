# WeatherPi
Python script that reads temp/humidity from a DHT11 sensor, and sends the data to APRS-IS

This program has been remixed from the source code listed on the Raspberry Pi and Stuff Wordpress site, accessible here. 
https://raspberrypiandstuff.wordpress.com/2017/08/07/uploading-aprscwop-weather-data/

The program will format the data received from a DHT11 sensor into an APRS packet, and sends the packet to an APRS server.

INSTALLATION
Open the .py file, and edit the lines as instructed by the comments. This program can be scheduled as a cron job to upload the data automatically.
