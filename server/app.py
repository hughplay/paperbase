import base64
import json
import io
import os
import random
from server.tool import PDFToolkit
import string
from datetime import datetime
from pathlib import Path

import requests
import numpy as np
from flask import Flask, request, send_file
from flask_cors import CORS
from flask_compress import Compress
from PIL import Image
from flask_mongoengine import MongoEngine

from .paper import Paper


# configuration
DEBUG = True


# instantiate the app
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["CORS_HEADERS"] = "Content-Type"
app.config['UPLOAD_FOLDER'] = "data/upload"
app.config["MONGODB_SETTINGS"] = {
    "db": "paper_database",
    "host": "localhost",
    "port": 27017,
}
Compress(app)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

db = MongoEngine(app)
toolkit = PDFToolkit()


@app.route("/api/papers", methods=["GET"])
def query_records():
    papers = Paper.objects()
    return {"papers": papers}


@app.route("/api/topic/<topic>", methods=["GET"])
def query_topic(topic):
    papers = Paper.objects(topic=topic)
    return {"papers": papers}


@app.route("/api/paper/<id>", methods=["GET"])
def query_record(id):
    paper = Paper.objects(id=id).first()
    if not paper:
        return {"error": "data not found"}
    else:
        return paper.to_json()


@app.route("/api/paper", methods=["PUT"])
def create_record():
    record = json.loads(request.data)
    paper = Paper(**record, index=Paper.objects.count())
    paper.save()
    return paper.to_json()


@app.route("/api/paper", methods=["POST"])
def update_record():
    record = json.loads(request.data)
    if 'date_update' in record:
        del record['date_update']
    if 'date_add' in record:
        del record['date_add']
    if '_id' in record:
        paper = Paper.objects(index=record["_id"]).first()
        del record['_id']
        if paper:
            paper.update(**record, date_update=datetime.utcnow)
            print(f'Update paper {paper["title"]}')
            return paper.to_json()
    paper = Paper(**record, index=Paper.objects.count())
    paper.save()
    print(f'Add paper {paper["title"]}')
    return paper.to_json()


@app.route("/api/paper/delete/<id>", methods=["GET"])
def delete_record(id):
    paper = Paper.objects(index=id).first()
    if not paper:
        return {"error": "data not found"}
    else:
        paper.update(removed=True)
        print(f'Remove paper {paper["title"]}')
    return paper.to_json()


@app.route("/api/paper/restore/<id>", methods=["GET"])
def restore_record(id):
    paper = Paper.objects(index=id).first()
    if not paper:
        return {"error": "data not found"}
    else:
        paper.update(removed=False)
        print(f'Restore paper {paper["title"]}')
    return paper.to_json()


def replace_filename(filename, len_random=7):
    time_str = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(
        [random.choice(string.ascii_lowercase) for _ in range(len_random)])
    new_name = time_str + random_str
    if '.' in filename:
        ext = filename.split('.')[-1]
        new_name = '.'.join([new_name, ext])
    return new_name


@app.route("/api/upload", methods=["Post"])
def upload_file():
    uploaded_files = request.files.getlist("file[]")
    new_filenames = []
    for file in uploaded_files:
        new_filename = replace_filename(file.filename)
        new_filenames.append(new_filename)
        file.save(
            os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
    return {'filenames': new_filenames}


@app.route("/api/fetch/<filename>", methods=["GET"])
def load_file(filename):
    path = os.path.realpath(
        os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print(path)
    if os.path.exists(path):
        return send_file(path)
    else:
        return 'file not found'


@app.route("/api/complete_info")
def complete_info():
    url = request.args.get('url')
    info = toolkit.url2info(url)
    return {
        'url': url,
        'paper': info
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2022)
