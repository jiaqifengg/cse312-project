from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
#from database.databaseModule import database
#from flask_socketio import SocketIO, send

import re

# Initialize Flask App

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

#database = database(app)
# Jieyi will update this later
# insert the default profile picture

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
    # will fix later once database connection is established in this file
    acc_exists = True 
    if acc_exists:
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
    # need to check if username exists and add to the database with a hashed password 
    
    # Jieyi will update this later
    #cur= mysql.connection.cursor()
    #cur.execute("INSERT INTO <database name> (username,password) VALUES (%s,%s)",(username,password))
    #mysql.connection.commit()
    #cur.close()

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