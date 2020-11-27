from gridfs import GridFS
from pymongo import MongoClient
from flask import Flask, make_response
from flask import request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load config from a .env file:
load_dotenv()
MONGO_URL = os.environ['MONGO_URL']
MONGO_DB = os.environ['DB']
DEBUG_SET = os.environ['DEBUG_SET']
HEADER_SEC = os.environ['HEADER_SEC']

mongo_client = MongoClient(MONGO_URL)
db = mongo_client[MONGO_DB]
grid_fs = GridFS(db)

meta_collection = db['meta_data']


@app.route('/', methods=['GET', 'PUT'])
def index():
    if request.headers['auth'] != HEADER_SEC:
        return jsonify(status = "Not Authorized"), 401
    file_name = request.args.get('file')

    if request.method == 'PUT':
        head = {}
        head_list = ['Host', 'User-Agent', 'Content-Type', 'Accept', 'Content-Length']
        try:
            for x in request.headers:
                if x[0] not in head_list:
                    head[x[0]] = x[1]
        except:
            pass
        secure_name = secure_filename(request.files['file'].filename)
        with grid_fs.new_file(filename=secure_name) as fp:
            fp.write(request.files['file'])
            file_id = fp._id
        
        if grid_fs.find_one(file_id) is not None:
            meta_collection.insert_one({ 'id': str(file_id), 'filename': secure_name, 'meta': [head] })
            return jsonify(status = 'File saved successfully', record=str(secure_name)), 200
        else:
            return jsonify(status = 'An Error Occurred'), 500

    if request.method == 'GET':
        grid_fs_file = grid_fs.find_one({'filename': file_name})
        response = make_response(grid_fs_file.read())
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
        return response    
