#example input that must be parsed
#$GPRMC,011304.000,A,3346.0217,N,08422.6801,W,0.20,6.33,220616,,,A*7B
"""
eg3. $GPRMC,220516,A,5133.82,N,00042.24,W,173.8,231.8,130694,004.2,W*70
              1    2    3    4    5     6    7    8      9     10  11 12


      1   220516     Time Stamp
      2   A          validity - A-ok, V-invalid
      3   5133.82    current Latitude
      4   N          North/South
      5   00042.24   current Longitude
      6   W          East/West
      7   173.8      Speed in knots
      8   231.8      True course
      9   130694     Date Stamp
      10  004.2      Variation
      11  W          East/West
      12  *70        checksum   
"""
#magpi.cc/1PxPopi influenced
import serial
import os

#set up serial connection to gps in usb port
ser = serial.Serial(
	port = '/dev/ttyUSB0',\
	baudrate = 4800,\
	parity = serial.PARITY_NONE,\
	stopbits = serial.STOPBITS_ONE,\
	bytesize = serial.EIGHTBITS,\
	timeout = 1)
#helper function to turn hemisphere lat/long -->decimal
def hemisphere_to_decimal(data, hemisphere):
	try:
		decimalPointPosition = data.index('.')
		degrees = float(data[:decimalPointPosition-2])
		minutes = float(data[decimalPointPosition-2:])/60
		output = degrees + minutes
		if hemisphere is 'N' or hemisphere is 'E':
			return output
		if hemisphere is 'S' or hemisphere is 'W':
			return -output
	except:
		return ""

#Helper function to take GPRMC sentence and parse it
def parse_GPRMC(data):
	data = data.split(',')
	dataDict = {
	['lat']
	
	}
	
