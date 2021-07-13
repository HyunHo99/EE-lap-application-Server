from pybo import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user = db.Column(db.Text(), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    post = db.relationship('Post', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user = db.Column(db.Text(), nullable=False)


class UserLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    labs = db.Column(db.Text(), nullable=False)
    user = db.Column(db.Text(), nullable=False)