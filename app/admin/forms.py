#coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FileField,SelectField,TextAreaField,SelectMultipleField
from wtforms.validators import DataRequired,ValidationError,EqualTo
from app.models import Admin
from app.models import Tag,Auth,Role
class LoginForm(FlaskForm):
    """管理员登录表单"""
    account=StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class":"form-control",
            "placeholder":"请输入账号！",
            "required":False,
        }
    )
    pwd=PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            "required": False,
        }
    )
    submit=SubmitField(
        "登录",
        render_kw={
            "class":"btn btn-primary btn-block btn-flat"
        }
    )
    def validate_account(self,field):
        account=field.data
        admin=Admin.query.filter_by(name=account).count()
        if admin==0:
            raise ValidationError("账号不存在")
class TagForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入标签")
        ],
        description="标签",
        render_kw={

            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"

        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )
class MovieForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.tag_id.choices = [(v.id, v.name) for v in Tag.query.all()]

    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名")
        ],
        description="片名",
        render_kw={

            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入片名！"

        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件")
        ],
        description="文件",

    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={

            "class": "form-control",
            "rows": 10

        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面")
        ],
        description="封面",

    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",

        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        description="标签",
        render_kw={
            "class": "form-control",

        }
    )



    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区!"

        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长!"

        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请输入上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间!",
            "id": "input_release_time"

        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class": "btn btn-primary"
        }
    )

class PreviewForm(FlaskForm):
    title = StringField(
        label="预告名称",
        validators=[
            DataRequired("请输入预告名称")
        ],
        description="预告名称",
        render_kw={

            "class": "form-control",
            "placeholder": "请输入预告名称！"

        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传预告封面")
        ],
        description="预告封面",

    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )

class PwdForm(FlaskForm):
    old_pwd=PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")

        ],
        description="旧密码",
        render_kw={
            "class":"form-control",
            "placeholder":"请输入旧密码",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")

        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码",
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            "class": "btn btn-primary"
        }
    )
    def validate_old_pwd(self,field):
        from flask import session
        pwd=field.data
        name=session["admin"]
        admin=Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误")

class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("请输入权限名称！")

        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称",
        }
    )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址！")

        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址",
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称！")

        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称",
        }
    )
    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("请选择权限列表！")

        ],
        coerce=int,
        description="权限列表",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.auths.choices = [(v.id,v.name)for v in Auth.query.all()]

class AdminForm(FlaskForm):
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("请输入管理员名称！")

        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称",
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("请输入管理员密码！")

        ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码",
        }
    )
    repwd = PasswordField(
        label="管理员重复密码",
        validators=[
            DataRequired("请输入管理员重复密码！"),
            EqualTo('pwd',message="两次密码不一致")

        ],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员重复密码",
        }
    )
    role_id=SelectMultipleField(
        label="所属角色",
        coerce=int,
        validators=[
            DataRequired("请添加管理员角色")

        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请添加管理员角色",
        }

    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary",

        }
    )

    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(v.id, v.name) for v in Role.query.all()]