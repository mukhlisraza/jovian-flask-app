from flask import Flask

app = Flask(__name__)
app.secret_key = 's3955809'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'alumni-management-s3955809'
