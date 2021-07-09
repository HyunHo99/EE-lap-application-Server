from flask import Blueprint
import json

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/',methods=['GET'])
def index():
    return json.dumps(["hi"])


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'