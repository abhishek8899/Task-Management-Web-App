import sqlite3

conn = sqlite3.connect('db/test.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS accounts(PID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME VARCHAR(100) NOT NULL, EMAIL VARCHAR(100) NOT NULL,PASSWARD VARCHAR(100) NOT NULL,SALT VARCHAR(100) NOT NULL,COMPLETED VARCHAR(100) )''')

c.execute('''CREATE TABLE IF NOT EXISTS users(PID INTEGER PRIMARY KEY AUTOINCREMENT,
EMAIL VARCHAR(100) NOT NULL,TASK VARCHAR(100) NOT NULL,STARTING VARCHAR(100),ENDING VARCHAR(100) NOT NULL,STATUS VARCHAR(100) NOT NULL,COLOR text NOT NULL)''')
c = conn.cursor()
conn.close()
