from flask import Flask, render_template, request, redirect
import sqlite3
import bcrypt
import test

emailg = "a"
login = False
loginuser = "a"
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/signup.html")
def main1():
    return render_template('signup.html')


@app.route("/login.html", methods=['POST', 'GET'])
def main2():
    global login
    print (login)
    if login is True:
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        global emailg
        cur.execute('SELECT * FROM accounts where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        return render_template('dashboard.html', data=row)
    else:
        return render_template('login.html')


@app.route("/logout", methods=['POST', 'GET'])
def main21():
    global login
    login = False
    return redirect('login.html')


@app.route("/send", methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        nnn = request.form['username']
        hashpassa = request.form['pass']
        cpass = request.form['conpass']
        nnnn = request.form['naam']
        cur.execute('SELECT * FROM accounts')
        rows = cur.fetchall()
        exis_user = None
        if hashpassa != cpass:
            return 'Confirm correct password'
        for row in rows:
            if nnn == row[2]:
                exis_user = 'a'
                break
        if exis_user is None:
            l = bcrypt.gensalt()
            hashpass = bcrypt.hashpw(hashpassa.encode('utf-8'), l)
            print(hashpass, nnn)
            cur.execute(
                "INSERT INTO accounts (NAME,EMAIL,PASSWARD,SALT) VALUES (?,?,?,?);", (nnnn, nnn, hashpass, l))
            conn.commit()
            cur.execute('SELECT * FROM accounts')
            rows = cur.fetchall()
            for row in rows:
                print(row)
            pass
            conn.close()

            return redirect('login.html')

        return 'That username already exists'

    return render_template('signup.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        taska = request.form['task']
        sd = request.form['sdate']
        ed = request.form['edate']
        kk = "TO DO"
        rowsq = None
        cur.execute('SELECT EMAIL FROM users where TASK = ?', (taska,))
        rowsq = cur.fetchall()
        flag = False
        global emailg
        for row in rowsq:
            print (row[0], emailg)
            if row[0] == emailg:
                flag = True
        if flag is False:
            cur.execute("INSERT INTO users (EMAIL,TASK,STARTING,ENDING,STATUS) VALUES (?,?,?,?,?);",
                        (emailg, taska, sd, ed, kk))
            conn.commit()
        cur.execute('SELECT * FROM users where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        conn.close()
        return render_template('dashboard.html', data=row)


@app.route('/dashboard.html', methods=['POST', 'GET'])
def dashboard():
    #print (request.method)
    if request.method == 'POST':
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        emala = request.form['ema']
        global emailg
        emailg = emala
        passa = request.form['pa']
        cur.execute('SELECT SALT FROM accounts where EMAIL = ?', (emala,))
        conn.commit()
        rows = cur.fetchall()
        if len(rows) is 0:
            conn.close()
            return 'username does not exist'
        rowsa = None
        cur.execute('SELECT PASSWARD FROM accounts where EMAIL = ?', (emala,))
        conn.commit()
        rowsa = cur.fetchall()
        if len(rowsa) is 0:
            conn.close()
            return 'the username or password is wrong'
        hashpass = rows[0][0]
        passa = bcrypt.hashpw(passa.encode('utf-8'), hashpass)
        if rowsa[0][0] == passa:
            global login
            #emailg = emala
            print (emailg, emala)
            login = True
            cur.execute('SELECT * FROM users where EMAIL = ?', (emailg,))
            row = cur.fetchall()
            conn.close()
            return render_template('dashboard.html', data=row)
        conn.close()
        return 'the username or password is wrong'
    return redirect('login.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
