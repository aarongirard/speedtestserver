#http://www.cyberciti.biz/faq/python-run-external-command-and-get-output/
#http://pastebin.com/WMEh802V
import os
import subprocess
import datetime
import time
import sqlite3 as sql

errOccur = 0

#set connection to DB
connection = sql.connect('SpeedTest.db')
cursor = connection.cursor()

while True:
	#record time
	ts = time.time() #get timestamp
	date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') #human readable time

	#run speed test, output is output variable
	p = subprocess.Popen("speedtest-cli --simple", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate() #data buffered in memory//will block next statement
	p_status = p.wait() #could use other method if want to check output real rime

	outputs = output.split('\n')
	
	#checks if speed test was successful
	if err is None and "Download" in output:
		#save data to db
		up = float(outputs[2].split(':')[1].split(' ')[1])
     		down = float(outputs[1].split(':')[1].split(' ')[1])
     		ping = float(outputs[0].split(':')[1].split(' ')[1])
        	values = (date, down, up, ping) 
        	cursor.execute('INSERT INTO tests(Date,Download_Speed,Upload_Speed,Ping) VALUES (?,?,?,?)', values)
		connection.commit() #commit insertion to DB
	else:
		#didn't write because of err or Download not in output
		#set error so it tries to test at a faster interval
		errOccur = 1
	#check speed again if there was an error at an earlier interval
	if errOccur == 0:
		dt = datetime.datetime.now() + datetime.timedelta(minutes=15) #delta controls bow interval length
	else:
		dt = datetime.datetime.now() + datetime.timedelta(minutes=5) #if err, try again in 5 mintues instead
	
	#don't finish while until entire process should run again
	while datetime.datetime.now() < dt:
		time.sleep(60) #times in seconds

#close DB connection should be alright not to close as long as transactions are done
#connection.close()
