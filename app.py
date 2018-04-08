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


@app.route("/send", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        conn = sqlite3.connect('db/test.db')
        cur = conn.cursor()
        nnn = request.form['username']
        hashpass = request.form['pass']
        cpass = request.form['conpass']
        #exis_user = accounts.find_one({'NAME': request.form['username']})
        cur.execute('SELECT * FROM accounts')
        rows = cur.fetchall()
        exis_user = None
        if hashpass != cpass:
            return 'Confirm correct password'            
        for row in rows:
            if nnn == row[1]:
                exis_user = 'a'
                break
        if exis_user is None:
            #   hashpass = bcrypt.hashpw(
            #   request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            #   users.insert(
            #   {'name': request.form['username'], 'password': hashpass})
            print (hashpass, nnn)
            cur.execute("INSERT INTO accounts (NAME,PASSWARD) VALUES (?,?);", (nnn, hashpass))
            conn.commit()
            cur.execute('SELECT * FROM accounts')
            rows = cur.fetchall()
            for row in rows:
                print (row)
            pass
            conn.close()

            return redirect('login.html')

        return 'That username already exists'

    return render_template('signup.html')


if __name__ == "__main__":
    app.debug = True
    app.run()


# @app.route('/show_account/')
#   def show_account():
#       logged_in = False
#       if not logged_in:
#           abort(401)
#       return "balance is ..."

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
