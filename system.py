from flask import Flask, render_template, redirect, request,session
import sqlite3
app = Flask(__name__)
app.secret_key = "SUNABACO"

@app.route('/')
def hello_world():
    return 'Hello, Flask World!'







if __name__  == "__main__":
    app.run(debug=True)