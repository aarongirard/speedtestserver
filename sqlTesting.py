import sqlite3 as sql

connection = sql.connect('SpeedTest.db')
cursor = connection.cursor()

stmt = 


cursor.execute('INSERT INTO tests(Date,Upload_Speed,Download_Speed,Ping) VALUES ("2",34.3,4.4,55.5)')

connection.commit()
connection.close()
