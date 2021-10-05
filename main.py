from flask import Flask, render_template

# Initialize Flask App
app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# Home page
@app.route('/')
def hello():
  return "Hello World!"

# Register page
@app.route('/auth/register')
def register():
  name = "test"
  return render_template('./static/index.html', title='Welcome', username=name)

# Run 0.0.0.0 on port 8080
if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True, port = 8080)
