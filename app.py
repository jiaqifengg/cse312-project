from flask import Flask, render_template, json, url_for, redirect, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user, login_user, logout_user, login_required
from flask_pymongo import PyMongo
import pymongo, os, re
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = '5008cafee462ca7c310116be'

client = MongoClient("mongodb://0.0.0.0:27017")
#KEEP FOR DOCKER ==> client = MongoClient("mongo")
database = client['rocketDatabase']
userCollection = database['users']
activeUsers = database['activeUsers']

socketio = SocketIO(app)

def html(stuff):
    return '<html><body>' + stuff + '</body></html>'

count = 0
@app.route("/")
def index():
    loginName = session.get('sessionName')
    if 'sessionName' in session:
        #print (session['sessionName'])
        countUsers = activeUsers.find({}, {"name"}).count()
        #print(countUsers)
        if countUsers < 1:
            activeUsers.insert_one({"name": session['sessionName']})
        return render_template('index.html')
    else:
        return render_template('notLoggedIn.html')

@app.route("/register", methods = ["POST", "GET"])
def register():

    msg = ''
    if request.method == "POST":
        name = request.form['registerName']
        password = request.form['registerPassword']
        

        if name:
            hashedPassword = generate_password_hash(password)
            user = userCollection.find_one({"name": name})

            if user:
                string = "<h3 style = '"'color: red'"'>Name already exists!</h3>"
                return html(string)
            else:
                newUser = userCollection.insert_one({"name": name, "password": hashedPassword})
                return redirect("/login")
        else:
            string = "<h3 style = '"'color: red'"'>Fill out the requirements!</h3>"
            return html(string)   

    return render_template("register.html", msg=msg)

@app.route("/login", methods = ["POST", "GET"])
def login():

    if request.method == "POST":
        name = request.form['loginName']
        inputPassword = request.form['loginPassword']
        
        foundUser = userCollection.find_one({"name": name})

        if foundUser == None:
            string = "<h3 style = '"'color: red'"'>Error, name isn't correctly spelt, or doesn't exist!</h3>"
            return html(string)
            
        name = foundUser['name']
        databasePassword = foundUser['password']

        test = check_password_hash(databasePassword, inputPassword)
        if test:
            session['sessionName'] = name
            return redirect('/')
        else:
            string = "<h3 style = '"'color: red'"'>Error, name or password do not match!</h3>"
            return html(string)
    else:    
        return render_template("login.html")

@app.route('/logout')
def home():
    session.pop('sessionName')
    activeUsers.delete_one({"name": session.get('sessionName')})
    return redirect('/')

if __name__ == '__main__':
  socketio.run(app)
  #app.run(debug=True)