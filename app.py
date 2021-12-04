from flask import Flask, render_template, json, url_for, redirect, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user, login_user, logout_user, login_required
from flask_pymongo import PyMongo
import pymongo
import os
import re
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = '5008cafee462ca7c310116be'

client = MongoClient(
    "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
# KEEP FOR DOCKER ==> client = MongoClient("mongo")
database = client['rocketDatabase']
userCollection = database['users']
activeUsers = database['activeUsers']

socketio = SocketIO(app)

users = {}


def html(stuff):
    return '<html><body>' + stuff + '</body></html>'


count = 0


@app.route("/")
def index():
    loginName = session.get('sessionName')
    if 'sessionName' in session:
        #print (session['sessionName'])
        countUsers = activeUsers.find({"name": session["sessionName"]}).count()
        # print(countUsers)
        if countUsers < 1:
            activeUsers.insert_one({"name": session['sessionName']})

        allActiveUsers = activeUsers.find({"name": {"$exists": True}})
        allUsers = []
        for user in allActiveUsers:
            allUsers.append(user["name"])
        return render_template('index.html', username=loginName, users=allUsers)
    else:
        return render_template('notLoggedIn.html')


@app.route("/register", methods=["POST", "GET"])
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
                newUser = userCollection.insert_one(
                    {"name": name, "password": hashedPassword})
                return redirect("/login")
        else:
            string = "<h3 style = '"'color: red'"'>Fill out the requirements!</h3>"
            return html(string)

    return render_template("register.html", msg=msg)


@app.route("/login", methods=["POST", "GET"])
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
    activeUsers.delete_one({"name": session.get('sessionName')})
    session.pop('sessionName')
    return redirect('/')


@socketio.on("user")
def connect_user(data):
    users[data] = request.sid


# when it recieve message print it and send it back to all the client in js file with the bucket "message"
@socketio.on('private_message')
def handle_message(data):

    sessionID = users[data["To"]]
    # custom data
    emit('private_message', data["username"] +
         ":" + data["msg"], room=sessionID)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
