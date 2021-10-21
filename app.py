from flask import Flask, render_template, request
from flask_mysqldb import MySQL
#from flask_socketio import SocketIO, send

import re

# Initialize Flask App

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

app.config['MYSQL_HOST'] = '0.0.0.0'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = '<database name>'

mysql = MySQL(app)

########## HOME PAGE ##########
@app.route('/')
def home():
  #cur = mysql.connection.cursor()

  #cur.execute('''CREATE TABLE database_test1 (id INTEGER, username VARCHAR(20), password VARCHAR(20))''')
  #mysql.connection.commit()

  print("DONE!")
  return render_template("./static/index.html")

########## LOGIN PAGE ##########
@app.route('/auth/login', methods = ["GET", "POST"])
def login():
  message = ''
  
  if request.method == "POST":
    message = 'login code here'
  else:
    return render_template('./auth/login.html')

########## REGISTER PAGE ##########
@app.route('/auth/register', methods = ["GET", "POST"])
def register():
  msg = ''
  
  if request.method == "POST" and 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    cur= mysql.connection.cursor()
    cur.execute("INSERT INTO <database name> (username,password) VALUES (%s,%s)",(username,password))
    mysql.connection.commit()
    cur.close()
    print("Success!")
  else:
    print("Form isn't filled out!")
  return render_template('./auth/register.html', msg=msg)

########## 404 PAGE ##########
@app.errorhandler(404) #Sets up custom 404 page!
def pageNotFound(e):
  return render_template("404.html"), 404

########## 500 PAGE ##########
@app.errorhandler(500) #Sets up custom 505 page!
def internalServerError(e):
  return render_template("500.html"), 500

########### Run 0.0.0.0 on port 8080 ##########
if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True, port = 8080)
  #socketio.run(app)