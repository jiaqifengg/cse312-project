from flask import Flask, render_template, request
#from flask_socketio import SocketIO, send
import re

# Initialize Flask App
app = Flask(__name__,
            template_folder='templates',
            static_folder='static')


# Home page
@app.route('/')
def hello():
  return render_template("./static/index.html")

# Register page

@app.route('/auth/login', methods = ["GET", "POST"])
def login():
  message = ''
  if 'name' in request.form and 'password' in request.form and request.method == 'POST':
    name = request.form['name']
    password = request.form['password']

    if name:
      msg = "Name already exists in database!"

@app.route('/auth/register', methods = ["GET", "POST"])
def register():
  message = ''
  if 'name' in request.form and 'password' in request.form and request.method == 'POST':
    name = request.form['name']
    password = request.form['password']

    if name:
      msg = "Name already exists in database!"

@app.errorhandler(404) #Sets up custom 404 page!
def pageNotFound(e):
  return render_template("404.html"), 404
  
@app.errorhandler(500) #Sets up custom 505 page!
def internalServerError(e):
  return render_template("500.html"), 500

# Run 0.0.0.0 on port 8080
if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True, port = 8080)
  #socketio.run(app)
