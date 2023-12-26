from os import path

from flask import send_from_directory

from core import app


@app.route('/storage/<name>')
def display_file(name):
    return send_from_directory(path.abspath(app.config["UPLOAD_FOLDER"]), name)
