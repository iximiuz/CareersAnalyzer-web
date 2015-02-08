from flask import Flask, render_template
import sqlite3
import os


def create_db_conn():
    return sqlite3.connect(app.config['DATABASE_URI'])


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'careers.db')
    # SERVER_NAME = 'careers-analyzer.codeideas.net'

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    from api import *
    app.run(port=5000, threaded=True, debug=True)
