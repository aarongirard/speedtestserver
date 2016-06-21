
import sqlite3 as sql
import csv

connection = sql.connect('SpeedTest.db')
cursor = connection.cursor()


#cursor.execute('INSERT INTO tests(Date,Upload_Speed,Download_Speed,Ping) VALUES ("2",34.3,4.4,55.5)')
#cursor.execute('INSERT INTO tests(Date,Upload_Speed,Download_Speed,Ping) VALUES ("2016-06-15 02:10:02",56.73,11.51,39.2)')
#open file
with open('../data.csv','r') as csvfile:
        #read file as csv
        reader = csv.reader(csvfile)
        for row in reader:
                #parse each row as an sql insert stmt
             	date = row[0]
             	up = float(row[3].split(':')[1].split(' ')[1])
             	down = float(row[2].split(':')[1].split(' ')[1])
             	ping = float(row[1].split(':')[1].split(' ')[1])
                values = (date, down, up, ping)
                cursor.execute('INSERT INTO tests(Date,Download_Speed,Upload_Speed,Ping) VALUES (?,?,?,?)', values)
connection.commit()
connection.close()
