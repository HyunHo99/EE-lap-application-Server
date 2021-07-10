from flask import Blueprint, request
import json
from datetime import datetime
from pybo.models import Post, Comment
from pybo import db


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/',methods=['GET'])
def index():
    return "hi"