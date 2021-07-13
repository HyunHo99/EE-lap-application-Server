from flask import Blueprint, request
import json
from datetime import datetime
from pybo.models import Post, Comment, UserLike
from pybo import db


bp = Blueprint('lab', __name__, url_prefix='/lab')


@bp.route('/<string:user_id>/',methods=['GET'])
def getLikedLabs(user_id):
    likedList = UserLike.query.filter(UserLike.user==user_id).all()
    if(len(likedList)==1 and len(likedList[0].labs)!=0):
        return json.dumps(likedList[0].labs)
    return json.dumps("")



@bp.route('/<string:user_id>/',methods=['POST'])
def addLikedLabs(user_id):
    labcode = request.form["labcode"]
    likedList = UserLike.query.filter(UserLike.user==user_id).all()
    if(len(likedList)==1):
        if(len(likedList[0].labs)!=0):
            likedList[0].labs +=","+labcode
        else:
            likedList[0].labs = labcode
    else:
        db.session.add(UserLike(labs = labcode, user=user_id))
    db.session.commit()
    return json.dumps("success")

@bp.route('/<string:user_id>/<string:labcode>/',methods=['DELETE'])
def removeLikedLabs(user_id, labcode):
    likedModel = UserLike.query.filter(UserLike.user==user_id).all()
    if(len(likedModel)==1):
        likedList = likedModel[0].labs.split(",")
        if(labcode in likedList):
            filtedList = [i for i in likedList if i != labcode]
            likedModel[0].labs=','.join(filtedList)
            db.session.commit()
            return json.dumps("success")


    return json.dumps("fail")