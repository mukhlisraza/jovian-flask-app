from flask import Flask, render_template, jsonify, request, flash,redirect, url_for,send_from_directory
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import database
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import pdfkit

app = database.app

mysql = MySQL(database.app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# home
@app.route('/')
def hello_workd():
  return render_template('home.html')


# Registeration
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerform', methods=['GET', 'POST'])
def registerform():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        if password != repassword:
            flash('Password does not match', 'error')
            return render_template('register.html')

        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
        count = cur.fetchone()[0]

        if count > 0:
            flash('User already available try another one!', 'error')
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur.execute('''
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        ''', (username, hashed_password))

        user_id = cur.lastrowid  # Get the ID of the registered user

        # Insert the user role into the roles table
        cur.execute('''
            INSERT INTO roles (role, user_id)
            VALUES (%s, %s)
        ''', ('alumni', user_id))

        mysql.connection.commit()
        cur.close()

        flash('Register successfully!', 'success')
        return render_template('login.html')

    else:
        return "something wrong"


# Import the Flask-Login module
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Define a user loader callback
@login_manager.user_loader
def load_user(id):
    # Implement logic to fetch the user from the database based on the provided ID
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        user = User(user_data[0], user_data[1], user_data[2])
        return user


@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/loginaction', methods=['GET', 'POST'])
def loginaction():
    # if current_user.is_authenticated:
    #     return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        user_data = cur.fetchone()
        cur.close()

        if user_data and bcrypt.check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect('/dashboard')
        else:
            flash('Invalid Credentials. Please try again.', 'error')
    
    return render_template('login.html')


# Create a logout view
@app.route('/logout')
def logout():
    logout_user()
    flash('Logout successfully.', 'success')
    return redirect('/login')

# Protect your views with login_required
@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT roles.role, users.username FROM roles
        INNER JOIN users ON roles.user_id = users.id
        WHERE users.id = %s
    ''', (current_user.id,))
    result = cur.fetchone()

    if not result or result[0] != 'alumni':
        flash('Unauthorized access. Please log in.', 'error')
        return redirect(url_for('login'))

    role, username = result

     # Get certificates for the logged-in user
    cur.execute('''
        SELECT * FROM documents
        WHERE user_id = %s AND document_type = 'certificate'
    ''', (current_user.id,))
    certificates = cur.fetchall()


     # Get degrees for the logged-in user
    cur.execute('''
        SELECT * FROM documents
        WHERE user_id = %s AND document_type = 'degree'
    ''', (current_user.id,))
    degrees = cur.fetchall()

    cur.close()

    return render_template('dashboard.html', username=username, certificates=certificates, degrees=degrees)

@app.route('/certificate/<int:certificate_id>')
@login_required
def certificate(certificate_id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT documents.*, users.username
        FROM documents
        INNER JOIN users ON documents.user_id = users.id
        WHERE documents.id = %s
    ''', (certificate_id,))
    certificate = cur.fetchone()
    cur.close()
    
    if degree:
        # Pass the degree details to the degree.html template
        return render_template('certificate.html', certificate=certificate)
    else:
        # Handle case when degree is not found
        flash('Certificate not found.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/download_degree/<int:document_id>')
@login_required
def download_degree(document_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM documents WHERE unique_number = %s', (document_id,))
    document = cur.fetchone()
    cur.close()

    if document:
        filename = document[5] + '.pdf'
        directory = 'static/files'
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        flash('Document not found.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/download_certificate/<int:document_id>')
@login_required
def download_certificate(document_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM documents WHERE unique_number = %s', (document_id,))
    document = cur.fetchone()
    cur.close()

    if document:
        filename = document[5] + '.pdf'
        directory = 'static/files'
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        flash('Document not found.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/degree/<int:degree_id>')
@login_required
def degree(degree_id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT documents.*, users.username
        FROM documents
        INNER JOIN users ON documents.user_id = users.id
        WHERE documents.id = %s
    ''', (degree_id,))
    degree = cur.fetchone()
    cur.close()
    
    if degree:
        # Pass the degree details to the degree.html template
        return render_template('degree.html', degree=degree)
    else:
        # Handle case when degree is not found
        flash('Degree not found.', 'error')
        return redirect(url_for('dashboard'))


@app.route('/verify/document', methods=['GET', 'POST'])
def verification():
    if request.method == 'POST':
        certificate_id = request.form['certificateID']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM documents WHERE unique_number = %s', (certificate_id,))
        certificate = cur.fetchone()
        cur.close()
        
        if certificate:
            # Get the user details for the certificate
            user_id = certificate[2]
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user = cur.fetchone()
            cur.close()
            
            if user:
                return render_template('verify.html', certificate=certificate, user=user)
            else:
                flash('User not found.', 'error')
                return render_template('home.html')
        else:
            flash('Certificate not found.', 'error')
            return render_template('home.html')
    
    return render_template('verify.html')


if __name__ == '__main__':
  app.run(debug=True)
