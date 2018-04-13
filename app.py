from flask import Flask, render_template, request, redirect
import sqlite3
import bcrypt
import test

login = False
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/signup.html")
def main1():
    return render_template('signup.html')


@app.route("/login.html" , methods=['POST', 'GET'])
def main2():
    global login
    login = False
    return render_template('login.html')


@app.route("/dashboard.html")
def main3():
    global login
    if login is True:
        return render_template('dashboard.html')
    else:
        return "YOU ARE NOT ALLOWED TO ENTER"


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
            hashpass = bcrypt.hashpw(hashpassa.encode('utf-8'),l)
            print( hashpass, nnn)
            cur.execute(
                "INSERT INTO accounts (NAME,EMAIL,PASSWARD,SALT) VALUES (?,?,?,?);", (nnnn, nnn, hashpass,l))
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
        if rows is None:
            return 'the username or password is wrong'
            pass
        hashpass = rows[0][0]
        passa = bcrypt.hashpw(passa.encode('utf-8'), hashpass)
        print(passa)

        rows = None
        cur.execute('SELECT PASSWARD FROM accounts where EMAIL = ?', (emala,))
        rows = cur.fetchall()
        if rows is None:
            return 'the username or password is wrong'
            pass
        if rows[0][0] == passa:
            global login
            login = True
            cur.execute('SELECT * FROM accounts where EMAIL = ?', (emala,))
            row = cur.fetchall()
            return render_template('dashboard.html', data=row)
            pass
        conn.close()

        return 'the username or password is wrong'
    return render_template('signup.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
