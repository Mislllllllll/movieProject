#coding:utf-8
from datetime import datetime
from app import db
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
#
# app=Flask(__name__)
# app.debug=True
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root1234.@127.0.0.1:3306/movie'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config["SECRET_KEY"]='b8cf3b1ea7354c5c954485e18784f2f0'
# db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    __table_args__={'extend_existing':True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(1024))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)
    userlogs = db.relationship('Userlog', backref='user')
    comments = db.relationship('Comment', backref='user')
    moviecols = db.relationship('Moviecol', backref='user')

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)


class Userlog(db.Model):
    __tabname__ = "userlog"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Userlog %r>" % self.id


#标签
class Tag(db.Model):
    __tablename__ = "tag"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    movies = db.relationship("Movie", backref='tag')

    def __repr__(self):
        return "<Tag %r>" % self.name


class Movie(db.Model):
    __tablename__ = "movie"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship("Comment", backref='movie')
    moviecols = db.relationship("Moviecol", backref='movie')

    def __repr__(self):
        return "<Movie %r>" % self.title


#上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Preview %r>" % self.title


class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  #所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id


#电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  #所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "Moviecol %r" % self.id


#权限
class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name


#角色
class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship("Admin", backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name


#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship("Adminlog", backref="admin")
    oplogs = db.relationship("Oplog", backref="admin")

    def __repr__(self):
        return "<Admin %r>" % self.name
    def check_pwd(self,pwd):
        from werkzeug.security import  check_password_hash
        return check_password_hash(self.pwd,pwd)




#管理员登录日志
class Adminlog(db.Model):
    __tabname__ = "adminlog"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Adminlog %r>" % self.id


#操作日志
class Oplog(db.Model):
    __tabname__ = "oplog"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  #所属管理员
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Oplog %r>" % self.id


# if __name__ == "__main__":
#     with app.app_context():
        # db.create_all()
        # role=Role(
        #         name="超级管理员",
        #         auths=""
        #     )
        # db.session.add(role)
        # db.session.commit()
        # from werkzeug.security import generate_password_hash
        #
        # admin = Admin(
        #     name="lyc",
        #     pwd=generate_password_hash('lyc'),
        # )
        # db.session.add(admin)
        # db.session.commit()
