from flask import Flask, render_template, request, redirect
import sqlite3
import bcrypt
import test
import os
import time
import datetime

emailg = "a"
login = False
loginuser = "a"
app = Flask(__name__)


UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/signup.html")
def main1():
    return render_template('signup.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    print ("file ",file)
    filename = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
    file.save(filename)
    print (filename, file)
    global emailg
    os.rename(filename, 'static/' + emailg + '.jpg')
    return redirect('profile.html')


@app.route("/login.html", methods=['POST', 'GET'])
def main2():
    global login
    #print (login)
    if login is True:
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        global emailg
        cur.execute('SELECT name FROM accounts where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        return render_template('dashboard.html', data=row)
    else:
        return render_template('login.html')


@app.route("/mytasks.html", methods=['POST', 'GET'])
def main3():
    global login
    #print (login)
    if login is True:
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        global emailg
        cur.execute('SELECT * FROM users where EMAIL = ?', (emailg,))
        r1 = cur.fetchall()
        cur.execute('SELECT pid,name FROM accounts where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        print ("row                   ", row)
        print ("r1                   ", r1)
        result = []
        name = emailg + '.jpg'
        path = 'static/'
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        if len(result) == 0:
            return render_template('mytasks.html', data=row, data1=r1, iimg='user.png')
        else:
            return render_template('mytasks.html', data=row, data1=r1, iimg=name)
    else:
        return redirect('login.html')


@app.route("/profile.html", methods=['POST', 'GET'])
def main4():
    global login
    if login is True:
        print ('ituwguiniunet roefer')
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        global emailg
        cur.execute('SELECT * FROM accounts where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        result = []
        name = emailg + '.jpg'
        path = 'static/'
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        if len(result) == 0:
            return render_template('profile.html', data=row, iimg='user.png')
        else:
            return render_template('profile.html', data=row, iimg=name)
    else:
        return redirect('login.html')


@app.route("/calendar.html", methods=['POST', 'GET'])
def main6():
    global login
    if login is True:
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        global emailg
        cur.execute('SELECT * FROM accounts where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        result = []
        name = emailg + '.jpg'
        path = 'static/'
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        if len(result) == 0:
            return render_template('calendar.html', data=row, iimg='user.png')
        else:
            return render_template('calendar.html', data=row, iimg=name)
    else:
        return redirect('login.html')


@app.route("/contact.html", methods=['POST', 'GET'])
def main7():
    global login
    if login is True:
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        global emailg
        cur.execute('SELECT * FROM accounts where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        result = []
        name = emailg + '.jpg'
        path = 'static/'
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        if len(result) == 0:
            return render_template('contact.html', data=row, iimg='user.png')
        else:
            return render_template('contact.html', data=row, iimg=name)
    else:
        return redirect('login.html')


@app.route("/information.html", methods=['POST', 'GET'])
def main5():
    global login
    if login is True:
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        global emailg
        cur.execute('SELECT * FROM accounts where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        result = []
        name = emailg + '.jpg'
        path = 'static/'
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        if len(result) == 0:
            return render_template('information.html', data=row, iimg='user.png')
        else:
            return render_template('information.html', data=row, iimg=name)
    else:
        return redirect('login.html')



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
        kk = request.form['typee']
        col = request.form['colora']
        if col == "1":
            colo = "#fe5e5e"
        elif col == "2":
            colo = "#fafeb9"
        else:
            colo = "#c7fdc5"
        rowsq = None
        cur.execute('SELECT EMAIL FROM users where TASK = ?', (taska,))
        rowsq = cur.fetchall()
        flag = False
        global emailg
        for row in rowsq:
            #print (row[0], emailg)
            if row[0] == emailg:
                flag = True
        if flag is False:
            cur.execute("INSERT INTO users (EMAIL,TASK,STARTING,ENDING,STATUS,COLOR) VALUES (?,?,?,?,?,?);",
                        (emailg, taska, sd, ed, kk,colo))
            conn.commit()
        cur.execute('SELECT * FROM users where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        conn.close()
        return redirect('mytasks.html')

@app.route('/index.html', methods=['POST', 'GET'])
def indi():
    return render_template('index.html');

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
            print (emailg, emala)
            login = True
            cur.execute('SELECT name FROM accounts where EMAIL = ?', (emailg,))
            row = cur.fetchall()
            conn.close()
            #print ("in dashboard  row  ", row)
            result = []
            name = emailg + '.jpg'
            print ('deknejnokdnlnklked             ', name)
            #print (name)
            path = 'static/'
            for root, dirs, files in os.walk(path):
                if name in files:
                    result.append(os.path.join(root, name))
            if len(result) == 0:
                return render_template('dashboard.html', data=row, iimg='user.png')
            else:
                return render_template('dashboard.html', data=row, iimg=name)
        conn.close()
        return 'the username or password is wrong'
    else:
        global login
        if login is False:
            return redirect('login.html')
        else:
            global emailg
            conn = sqlite3.connect('db/test.db')
            cur = conn.cursor()
            cur.execute('SELECT name FROM accounts where EMAIL = ?', (emailg,))
            row = cur.fetchall()
            conn.close()
            result = []
            name = emailg + '.jpg'
            path = 'static/'
            for root, dirs, files in os.walk(path):
                if name in files:
                    result.append(os.path.join(root, name))
            if len(result) == 0:
                return render_template('dashboard.html', data=row, iimg='user.png')
            else:
                return render_template('dashboard.html', data=row, iimg=name)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        se = request.form['searching']
        option = request.form['sea']
        print(se)
        if option is "1":
            cur.execute('SELECT * FROM users where STATUS = ? and EMAIL= ?', (se,emailg,))
        else:
            cur.execute('SELECT * FROM users where TASK = ? and EMAIL = ? ', (se,emailg,))
        r1 = cur.fetchall()
        cur.execute('SELECT pid,name FROM accounts where EMAIL = ?', (emailg,))
        row = cur.fetchall()
        print (r1,row)
        conn.close()
        result = []
        name = emailg + '.jpg'
        path = 'static/'
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
        if len(result) == 0:
            return render_template('mytasks.html', data=row, data1=r1, iimg='user.png')
        else:
            return render_template('mytasks.html', data=row, data1=r1, iimg=name)


if __name__ == "__main__":
    conn = sqlite3.connect('db/test.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    row = cur.fetchall()
    for x in row:
        newdate1 = time.strptime(str(x[3]), "%Y-%m-%d")
        newdate2 = time.strptime(str(x[4]), "%Y-%m-%d")
        now = datetime.date.today()
        now = str(now)
        # print(now)
        date = time.strptime(now, "%Y-%m-%d")
        # print(date)
        if(newdate1 < date):
            print (x[3],now)
            cur.execute(
                'UPDATE users SET STATUS = "TO DO" where EMAIL = ?', (x[1],))
            conn.commit()
            pass
        if newdate1 >= date and newdate2 <= date:
            cur.execute(
                'UPDATE users SET STATUS = "IN PROGRESS" where EMAIL = ?', (x[1],))
            conn.commit()
        if newdate2 > date:
            cur.execute(
                'UPDATE users SET STATUS="DONE" where EMAIL = ?', (x[1],))
            conn.commit()
    conn.close()
    app.debug = True
    app.run()
