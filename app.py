import os
import sys

from flask import Flask

from game.runserver import bp

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.register_blueprint(bp)
    app.run(port=8081)