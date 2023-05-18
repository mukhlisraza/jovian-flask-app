from flask import Flask, render_template, jsonify, request, flash,redirect, url_for
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import database

app = database.app

mysql = MySQL(database.app)

@app.route('/')
def hello_workd():
  return render_template('home.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/loginaction', methods=['GET', 'POST'])
def loginaction():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            flash('Invalid Credentials. Please try again.', 'error')
            return render_template('login.html')
        else:
            return redirect('/')
    return render_template('login.html', error=error)

@app.route('/register')
def register():
  return render_template('register.html')

bcrypt = Bcrypt()
@app.route('/registerform', methods=['GET', 'POST'])
def registerform():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        if password != repassword:
            flash('Password does not match', 'error')
            return render_template('.html',)
        else:
            cur = mysql.connection.cursor()
            cur.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
            count = cur.fetchone()[0]
           
            if count > 0:
              flash('User already available try other one!', 'error')
              return render_template('register.html',)
            else:
              hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

              user = [{
                'username': username,
                'password': hashed_password,
              }]
              cur.executemany('''
                  INSERT INTO users (username, password)
                  VALUES (%(username)s, %(password)s)
              ''', user)
              mysql.connection.commit()
              cur.close()

              flash('Register successfully!', 'success')
              return render_template('login.html',)
    else:
       return "something differnt"


if __name__ == '__main__':
  app.run(debug=True)
