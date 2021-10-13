from flask import Flask, render_template, request
#from flask_socketio import SocketIO, send

import re

# Initialize Flask App

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

app.config['MYSQL_HOST'] = '0.0.0.0'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''


#mysql = MySQL(app)

########## HOME PAGE ##########
@app.route('/')
def home():
  return render_template("./static/index.html")

########## LOGIN PAGE ##########
@app.route('/auth/login', methods = ["GET", "POST"])
def login():
  message = ''
  if 'name' in request.form and 'password' in request.form and request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    if name:
      msg = "Name already exists in database!"
    elif email:
      msg = "Email already exists in database!"
    else:
      msg = "Success!"

########## REGISTER PAGE ##########
@app.route('/auth/register', methods = ["GET", "POST"])
def register():
  if request.method == 'POST':
    ## if statement needs to be modified

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

  for entries in request.form:
    print("entries are ", entries)

  return render_template("./auth/register.html")

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