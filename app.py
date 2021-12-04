from flask import Flask
from flask import request
from flask import render_template
import time
import asyncio


app = Flask(__name__)

async def long_load(typeback):
    time.sleep(5) #just simulating the waiting period
    return "You typed: %s" % typeback

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/loading', methods=['POST'])
def loading():
    return render_template ("loading.html")

@app.route('/task')
async def task():
    #query = request.form['anything']
    query = "oh"
    final_file =  await long_load(query)
    return render_template("done.html", display=final_file)


if __name__ == '__main__':
    #app.debug = True
    app.run()