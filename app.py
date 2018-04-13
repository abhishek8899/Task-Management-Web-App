from flask import Flask, render_template, request, redirect
import sqlite3
import bcrypt
import test
emailg = "dsasdds"

login = False
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
    login = False
    return render_template('login.html')


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
            la = bcrypt.gensalt()
            hashpass = bcrypt.hashpw(hashpassa.encode('utf-8'), la)
            print(hashpass, nnn)
            cur.execute(
                "INSERT INTO accounts (NAME,EMAIL,PASSWARD,SALT) VALUES (?,?,?,?);", (nnnn, nnn, hashpass, la))
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


@app.route('/dashboard.html', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        emala = request.form['ema']
        passa = request.form['pa']
        cur.execute('SELECT SALT FROM accounts where EMAIL = ?', (emala,))
        rows = cur.fetchall()
        if len(rows) is 0:
            return 'the username or password is wrong'
            pass
        rowsa = None
        cur.execute('SELECT PASSWARD FROM accounts where EMAIL = ?', (emala,))
        rowsa = cur.fetchall()
        print(rowsa)
        print(rows)
        if len(rowsa) is 0:
            return 'the username or password is wrong'
            pass
        hashpass = rows[0][0]
        passa = bcrypt.hashpw(passa.encode('utf-8'), hashpass)
        print(passa)
        if rowsa[0][0] == passa:
            global login
            global emailg
            emailg = emala
            login = True
            cur.execute('SELECT * FROM users where EMAIL = ?', (emala,))
            row = cur.fetchall()
            return render_template('dashboard.html', data=row)
            pass
        conn.close()

        return 'the username or password is wrong'
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
        global emailg
        cur.execute(
            "INSERT INTO users (EMAIL,TASK,STARTING,ENDING,STATUS) VALUES (?,?,?,?,?);", (emailg, taska, sd, ed, kk))
        conn.commit()
        cur.execute('SELECT * FROM users where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        conn.close()
        return render_template('dashboard.html', data=row)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        se = request.form['searching']
        cur.execute('SELECT * FROM users where TASK = ?', (se,))
        row = cur.fetchall()
        conn.close()
        return render_template('dashboard.html', data=row)


if __name__ == "__main__":
    app.debug = True
    app.run()
