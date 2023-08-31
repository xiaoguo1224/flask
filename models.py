from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    create_time = db.Column(db.DateTime, default=datetime.now)


class EmailCapture(db.Model):
    __tablename__ = 'email_capture'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    capture = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    # isUse = db.Column(db.Integer, default=0)


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    context = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 添加联系,backref是反向引用，lazy='dynamic'表示动态加载，即查询所有文章
    # 在访问article时可以反馈对应的user对象，并且加了backref可以实现双向绑定
    author = db.relationship("UserModel", backref=db.backref("question", lazy="dynamic"))
