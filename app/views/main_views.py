from flask import Blueprint, render_template

from app.models import Question

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def hello_pybo():
    return "hi"