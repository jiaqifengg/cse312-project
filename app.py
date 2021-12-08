from flask import Flask, render_template, json, url_for, redirect, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
#from flask_login import current_user, login_user, logout_user, login_required
#from flask_pymongo import PyMongo
#import pymongo
import os
import re
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, CSRFError

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = '5008cafee462ca7c310116be'
csrf = CSRFProtect(app)
# change this to whatever you use locally if you test locally
client = MongoClient("mongo") 
# KEEP FOR DOCKER ==>
# client = MongoClient("mongo")  # for docker
database = client['rocketDatabase']
userCollection = database['users']
activeUsers = database['activeUsers']


allowedImageExtensions = {'png', 'jpg', 'jpeg', 'gif'}
socketio = SocketIO(app)

users = {}
usersMessages = {}
post_count = [0]
posts = {}
# {id: post:"", upvote:{username:username}, downvote:{username:username}}
# using dictionary for upvote/downvote for O(1) access of who has voted


def html(stuff):
    return '<html><body>' + stuff + '</body></html>'


def cleanHTML(content):
    return content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('\"', '&quot;').replace('\'', '&#39;')


count = 0
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf.html'), 400

@app.route("/")
def index():
    loginName = session.get('sessionName')
    print(loginName)
    if 'sessionName' in session:
        #print (session['sessionName'])
        #countUsers = activeUsers.find({"name": session["sessionName"]}).count()
        countUsers = activeUsers.count_documents(
            {"name": session["sessionName"]})
        # print(countUsers)
        if countUsers < 1:
            activeUsers.insert_one({"name": session['sessionName']})

        allActiveUsers = activeUsers.find({"name": {"$exists": True}})
        allUsers = []
        for user in allActiveUsers:
            if(user["name"] != session.get("sessionName")):
                allUsers.append(user["name"])
        return render_template('index.html', users=allUsers)
    else:
        return render_template('notLoggedIn.html')


@app.route("/members")
def members():
    return render_template("members.html")


@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":
        name = request.form['registerName']
        password = request.form['registerPassword']

        passwordLength = len(password)
        uppercaseLetter = re.search('[A-Z]', password)
        number = re.search('[0-9]', password)
        special = re.search('[ ~!@#$%^.&*()}{\/_:?<> ]', password)

        if passwordLength < 8:
            string = "<h3 style = '"'color: red'"'>Password needs at least 8 characters!</h3>"
            return html(string)
        elif uppercaseLetter == None:
            string = "<h3 style = '"'color: red'"'>Password needs at least 1 uppercase character!</h3>"
            return html(string)
        elif number == None:
            string = "<h3 style = '"'color: red'"'>Password needs at least 1 number!</h3>"
            return html(string)
        elif special == None:
            string = "<h3 style = '"'color: red'"'>Password needs at least 1 special character!</h3>"
            return html(string)

        hashedPassword = generate_password_hash(password)
        user = userCollection.find_one({"name": name})

        if user:
            string = "<h3 style = '"'color: red'"'>Name already exists!</h3>"
            return html(string)
        else:
            newUser = userCollection.insert_one(
                {"name": name, "password": hashedPassword})
            return redirect("/login")

    return render_template("register.html")


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
            string = "<h3 style = '"'color: red'"'>Password is incorrect!</h3>"
            return html(string)
    else:
        return render_template("login.html")


@app.route("/settings")
def settings():
    return render_template('settings.html')


@app.route("/settings", methods=["POST", "GET"])
def uploadImage():
    if request.method == "POST":
        if 'file' not in request.files:
            return 'no file part'
        imageFile = request.files['file']
        test = imageFile.filename
        print(imageFile)


@app.route('/logout')
def home():
    print("logout")
    # activeUsers.delete_one({"name": session.get('sessionName')})
    session.pop('sessionName')
    return redirect('/')

########## 404 PAGE ##########


@app.errorhandler(404)  # Sets up custom 404 page!
def pageNotFound(e):
    return render_template("404.html"), 404

########## 500 PAGE ##########


@app.errorhandler(500)  # Sets up custom 500 page!
def internalServerError(e):
    return render_template("500.html"), 500


# when client go to "connected" give the username to the client that is connected on "connected"
@socketio.on("connect")
def connected():
    print("connected: ", session.get("sessionName"))
    emit("connected", session.get("sessionName"))
    # use broadcast = true for broadcast to everyone
    # emit("updateOnlineUsers", session.get("sessionName"))


@socketio.on("user")
def connect_user(data):
    print("CONNECT USER DATA IS:", data)
    users[data] = request.sid


# when it recieve message print it and send it back to all the client in js file with the bucket "message"
@socketio.on('private_message')
def handle_message(data):

    name = data.get('To')
    if name not in users or name == session.get("sessionName"):
        emit('private_message', 'Error, name doesn\'t exist!')
        return 'error'

    sessionID = users[data["To"]]
    currentUserSessionID = users[session.get("sessionName")]
    # custom data

    sanitizedMessage = cleanHTML(data['msg'])
    emit('private_message', session.get("sessionName") +
         ":" + sanitizedMessage, room=sessionID)
    emit('curent_user_message', session.get("sessionName") +
         ":" + sanitizedMessage, room=currentUserSessionID)


@socketio.on("disconnect")
def disconnect():
    print("disconnected: ", session.get("sessionName"))
    del users[session.get("sessionName")]
    activeUsers.delete_one({"name": session.get('sessionName')})
    session.pop('sessionName')
    print(session.get("sessionName"))
    print(users)


@socketio.on('make_post')
def insertPost(data):
    userPicture = ""
    username = session.get('sessionName')
    post = data.get('post')
    temp = {
        "post": post,
        "user": [username, userPicture],
        "upvotes": {},
        "downvotes": {}
    }
    posts[post_count[0]] = temp
    post_count[0] += 1
    emit('make_post', temp, broadcast=True)


if __name__ == '__main__':

    # while using docker-compose, change debug to true if you want to test locally
    socketio.run(app, debug=False, port=5000, host="0.0.0.0")
    # app.run(debug=True)
