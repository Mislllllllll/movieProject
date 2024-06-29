import os.path

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flasgger import  Swagger


app=Flask(__name__)
Swagger(app)
app.debug=True
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root1234.@127.0.0.1:3306/movie'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"]='b8cf3b1ea7354c5c954485e18784f2f0'
app.config["UP_DIR"]=os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/")
app.config["FC_DIR"]=os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/users/")

db = SQLAlchemy(app)
app.debug=True

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint,url_prefix="/admin")

@app.errorhandler(404)
def ppage_not_found(error):
    return render_template("home/404.html"),404