#coding:utf-8
from . import home
from flask import render_template,redirect,url_for,flash,session,request
from app.home.forms import RegistForm,LoginForm,UserDetailForm,PwdForm
from app.models import User,Userlog,Preview,Tag,Movie
import uuid
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import db,app
from functools import wraps
import os
import datetime
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "user" not in session:
            return redirect(url_for("home.login",next=request.url))
        return f(*args,**kwargs)
    return decorated_function

#修改文件名称
def change_filename(filename):
    fileinfo=os.path.splitext(filename)
    filename=datetime.datetime.now().strftime("%Y%m%d%H%M%S")+(uuid.uuid4().hex)+fileinfo[-1]
    return filename

@home.route("/login/",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        data=form.data
        user=User.query.filter_by(name=data["name"]).first()
        if not user.check_pwd(data["pwd"]):
            flash("密码错误",'err')
            return redirect(url_for("home.login"))
        session["user"]=user.name
        session["user_id"]=user.id
        userlog=Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html",form=form)


@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))

@home.route("/register/",methods=["GET","POST"])
def register():
    form=RegistForm()
    if form.validate_on_submit():
        data=form.data
        user=User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功",'ok')
        return redirect(url_for('home.login'))
    return render_template("home/register.html",form=form)


@home.route("/user/",methods=['GET','POST'])
@user_login_req
def user():
    form=UserDetailForm()
    user=User.query.get(int(session["user_id"]))
    form.face.validators=[]
    if request.method=="GET":
        form.name.data=user.name
        form.email.data=user.email
        form.phone.data=user.phone
        form.info.data=user.info
    if form.validate_on_submit():
        data=form.data
        file_face = secure_filename(form.face.data.filename)
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])
            os.chmod(app.config["FC_DIR"], "rw")
        user.face = change_filename(file_face)
        form.face.data.save(app.config["FC_DIR"] + user.face)
        name_count=User.query.filter_by(name=data["name"]).count()
        if data["name"]!=user.name and name_count==1:
            flash("昵称已经存在",'err')
            return redirect(url_for("home.user"))
        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"]!=user.email and email_count==1:
            flash("邮箱已经存在",'err')
            return redirect(url_for("home.user"))
        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"]!=user.phone and phone_count==1:
            flash("电话号码已经存在",'err')
            return redirect(url_for("home.user"))


        user.name=data["name"]
        user.email=data["email"]
        user.phone=data["phone"]
        user.info=data["info"]
        db.session.add(user)
        db.session.commit()
        flash("修改成功","ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html",form=form,user=user)

@home.route("/pwd/",methods=["GET","POST"])
@user_login_req
def pwd():
    form=PwdForm()
    if form.validate_on_submit():
        data=form.data
        user=User.query.filter_by(name=session["user"]).first()
        if not user.check_pwd(data["old_pwd"]):
            flash("旧密码错误",'err')
            return redirect(url_for('home.pwd'))
        user.pwd=generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功,请重新登录","ok")
        redirect(url_for('home.logout'))
    return render_template("home/pwd.html",form=form)


@home.route("/comments/")
@user_login_req
def comments():
    return render_template("home/comments.html")

@home.route("/loginlog/<int:page>/",methods=["GET"])
@user_login_req
def loginlog(page=None):
    if page is None:
        page=1
    page_data=Userlog.query.join(
        User
    ).filter(
        User.id==Userlog.user_id
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template("home/loginlog.html",page_data=page_data)

    return render_template("home/loginlog.html")

@home.route("/moviecol/")
@user_login_req
def moviecol():
    return render_template("home/moviecol.html")


@home.route("/<int:page>/",methods=["GET"])
def index(page=None):
    tags=Tag.query.all()
    page_data=Movie.query
    tid = request.args.get("tid", 0)
    if int(tid)!=0:
        page_data=page_data.filter_by(tag_id=int(tid))

    star=request.args.get("star",0)
    if int(star)!=0:
        page_data=page_data.filter_by(star=int(star))

    time=request.args.get("time",0)
    if int(time)!=0:
        if int(time)==1:

            page_data=page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    pm=request.args.get("pm", 0)
    if int(pm) != 0:
        if int(pm) == 1:

            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )
    cm=request.args.get("cm",0)
    if int(cm) != 0:
        if int(cm) == 1:

            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    if page is None:
        page=1
    page_data=page_data.paginate(page=page,per_page=10)
    p=dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm,
    )
    return render_template("home/index.html",tags=tags,p=p,page_data=page_data)
@home.route("/animation/")
def animation():
    data=Preview.query.all()
    for v in data:
        v.id=v.id-1
    return render_template("home/animation.html",data=data)


@home.route("/search/")
def search():
    return render_template("home/search.html")


@home.route("/play/")
def play():
    return render_template("home/play.html")

