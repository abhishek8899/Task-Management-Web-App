import sqlite3

conn = sqlite3.connect('db/test.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS accounts(PID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME VARCHAR(100) NOT NULL, EMAIL VARCHAR(100) NOT NULL,PASSWARD VARCHAR(100) NOT NULL )''')
conn.close()
