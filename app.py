from flask import Flask
from flask import request
from flask import render_template
import time

app = Flask(__name__)

def long_load(typeback):
    time.sleep(32) #just simulating the waiting period
    return "You typed: %s" % typeback

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/loading', methods=['POST'])
def loading():
    return render_template ("loading.html")

@app.route('/task')
def task():
    #query = request.form['anything']
    query = "oh"
    outcome = long_load(query)
    return render_template("done.html", display=outcome)


if __name__ == '__main__':
    #app.debug = True
    app.run()