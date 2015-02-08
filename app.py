from flask import Flask, render_template
import sqlite3
import os


def create_db_conn():
    return sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'careers.db'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    from api import *
    app.run(port=5050, threaded=True)
