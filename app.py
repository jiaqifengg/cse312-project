from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from database.user_auth import password_vaild, username_vaild
from database.databaseModule import database
from database.dbconfig import Dbconfig 
from flask_mysqldb import MySQL
#from flask_socketio import SocketIO, send

import re


# Initialize Flask App

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

app.config['MYSQL_HOST'] = Dbconfig.DATABASE_CONFIG['host']
app.config['MYSQL_USER'] = Dbconfig.DATABASE_CONFIG['user']
app.config['MYSQL_PASSWORD'] = Dbconfig.DATABASE_CONFIG['password']
app.config['MYSQL_DB'] = Dbconfig.DATABASE_CONFIG['database']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
mycursor = mysql.connection.cursor()
create_user_info_table = "CREATE TABLE IF NOT EXISTS account ("
create_user_info_table += "ID MEDIUMINT NOT NULL AUTO_INCREMENT, "
create_user_info_table += "username VARCHAR(50) NOT NULL, "
create_user_info_table += "hashed_password BLOB NOT NULL, "
create_user_info_table += "profile_pic_path VARCHAR(225) NOT NULL DEFAULT '', "  
create_user_info_table += "hashed_token_binary BLOB DEFAULT NULL, "
create_user_info_table += "exist_status BOOLEAN DEFAULT TRUE"
create_user_info_table += "PRIMARY KEY (ID, username)"
create_user_info_table += "); "
mycursor.execute(create_user_info_table)
mysql.commit()  


########## HOME PAGE ##########
@app.route('/')
def home():
  print("DONE!")
  return render_template("./static/index.html")

########## LOGIN PAGE ##########
@app.route('/auth/login', methods = ["GET", "POST"])
def login():
  message = ''
  if request.method == "POST" and 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']

    # check if an account exists 
    acc_exists = mysql.check_username_exist(username)
    if acc_exists:
      # check the password if it's vaild
      # to be discussed on what to do once user logs in
      pass
    else:
      message = 'Incorrect username or password'
  
  return render_template('./auth/login.html')

########## REGISTER PAGE ##########
@app.route('/auth/register', methods = ["GET", "POST"])
def register():
  msg = ''
  
  if request.method == "POST" and 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    
    msg = "Register successfully."

    # check if the username exist
    if mysql.check_username_exist(username):
      msg = 'Username already exists.'
      return render_template('./auth/register.html', msg=msg)
    # check the username
    check_username = username_vaild(username)
    if not check_username[0]:
      msg = check_username[1]
      return render_template('./auth/register.html', msg=msg)
    # check password
    check_password = password_vaild(password)
    if not check_password[0]:
      msg = check_password[1]
      return render_template('./auth/register.html', msg=msg)

  else:
    msg = "Please fill out the form."
    print("Form isn't filled out!")

  # successfully register
  # store username and password in database
  db.register(username, password)
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