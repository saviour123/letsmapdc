#!/usr/bin/env python

from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/w3w')
def w3w():
    return render_template('w3w.html')


if __name__ == "__main__":
    app.run(debug=True, port=2000)
