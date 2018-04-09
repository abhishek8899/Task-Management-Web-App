from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/signup.html")
def main1():
    return render_template('signup.html')


@app.route("/login.html")
def main2():
    return render_template('login.html')


@app.route("/dashboard.html")
def main3():
    return render_template('dashboard.html')


@app.route("/send", methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        nnn = request.form['username']
        hashpass = request.form['pass']
        cpass = request.form['conpass']
        nnnn = request.form['naam']
        cur.execute('SELECT * FROM accounts')
        rows = cur.fetchall()
        exis_user = None
        if hashpass != cpass:
            return 'Confirm correct password'
        for row in rows:
            if nnn == row[2]:
                exis_user = 'a'
                break
        if exis_user is None:
            #   hashpass = bcrypt.hashpw(
            #   request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            print(hashpass, nnn)
            cur.execute(
                "INSERT INTO accounts (NAME,EMAIL,PASSWARD) VALUES (?,?,?);", (nnnn, nnn, hashpass))
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


#  @app.route('/test1/')
# def test1():
#     fname = 'welcome'
#     return redirect(url_for(fname))

# @app.route('/test2/')
# def test2():
#     fname, name = 'welcome', 'foo'
#     return redirect (url_for(fname, name = name))

# @app.route('/welcome/')
# @app.route('/welcome/<name>')
# def welcome(name = None):
#     if name is None:
#         return "<h2 style=color:green>Hello %s !</h2>" % "Unknown User"
#     else:
#         return "<h2 style=color:green>Hello %s !</h2>" % name
