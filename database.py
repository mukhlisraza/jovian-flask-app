from flask import Flask

app = Flask(__name__)
app.secret_key = 'jovian-flask-app'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'alumni-management'
