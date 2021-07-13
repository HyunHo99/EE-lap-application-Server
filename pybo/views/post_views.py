from flask import Blueprint, request
import json
from datetime import datetime
from pybo.models import Post, Comment
from pybo import db


bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/main/<int:page_num>/',methods=['GET'])
def index(page_num):
    if(page_num<1):
        return "getOut"
    posts=Post.query.order_by(Post.create_date.desc())[(page_num-1)*10:page_num*10]
    data = []
    diction = {}
    for i in posts:
        data.append({"id":i.id, "subject":i.subject,"create_date":i.create_date.strftime("%m/%d/%Y, %H:%M:%S"), "content":i.content[:80]})
    diction["data"]=data
    diction["totalNum"]=Post.query.count()
    return json.dumps(diction)  



@bp.route('/',methods=['POST'])
def hello_pybo():
    Subject = request.form["subject"]
    Content = request.form["content"]
    User = request.form["user"]
    Create_date = datetime.now()
    p=Post(subject = Subject, content = Content, create_date = Create_date, user = User)
    db.session.add(p)
    db.session.commit()
    return json.dumps(['successed'])


@bp.route('/<int:post_id>/', methods=['GET'])
def return_comments(post_id):
    comments = Post.query.get(post_id).comment_set
    data = []
    diction = {}
    for i in comments:
        data.append({"content":i.content, "create_date":i.create_date.strftime("%m/%d/%Y, %H:%M:%S"), "id":i.id, "user":i.user})
    p = Post.query.get(post_id)
    diction["post"]={"subject":p.subject,"content":p.content, "create_date":p.create_date.strftime("%m/%d/%Y, %H:%M:%S"),"user":p.user}
    diction["data"]=data
    return json.dumps(diction)


@bp.route('/<int:post_id>/',methods=['POST'])
def add_comments(post_id):
    q = Post.query.get_or_404(post_id)
    commentContent = request.form["content"]
    User = request.form["user"]
    comments = Comment(content=commentContent, create_date = datetime.now(), user=User)
    q.comment_set.append(comments)
    db.session.commit()
    return json.dumps({"content":comments.content, "create_date":comments.create_date.strftime("%m/%d/%Y, %H:%M:%S"),"id":comments.id, "user":comments.user})


@bp.route('/<int:post_id>/',methods=['DELETE'])
def delete_post(post_id):
    q = Post.query.get_or_404(post_id)
    for i in q.comment_set:
        db.session.delete(i)
    db.session.delete(q)
    db.session.commit()
    return json.dumps(["success"])

@bp.route('/delete/<int:comment_id>/',methods=['DELETE'])
def delete_comment(comment_id):
    c = Comment.query.get_or_404(comment_id)
    db.session.delete(c)
    db.session.commit()
    return json.dumps(["success"])


@bp.route('/search/<string:keyWord>/',methods=['GET'])
def search_post(keyWord):
    if(len(keyWord)>=2 and len(keyWord)<=10):
        searchedPost = Post.query.filter(
            Post.subject.contains(keyWord)|Post.content.contains(keyWord)).order_by(Post.create_date.desc())
        data = []
        diction = {}
        for i in searchedPost:
            data.append({"id":i.id, "subject":i.subject,"create_date":i.create_date.strftime("%m/%d/%Y, %H:%M:%S"), "content":i.content[:80]})
        diction["data"]=data
        return json.dumps(diction)
    return "getOut"
    

