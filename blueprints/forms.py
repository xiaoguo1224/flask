import time
from datetime import datetime

import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, EmailCapture


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=4, max=12, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=40, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("邮箱已被注册！")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        verify_capture = EmailCapture.query.filter_by(capture=captcha, email=email).first()
        # print(date + " " + now)
        # print(date < now)
        # isUse = verify_capture.isUse
        if not verify_capture:
            raise wtforms.ValidationError("验证码错误！")
        date = verify_capture.date
        if date < datetime.now():
            raise wtforms.ValidationError("验证码已过期！")


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=40, message="密码格式错误")])

    def validate_password(self, field):
        email = self.email.data
        password = field.data
        login = UserModel.query.filter_by(email=email, password=password).first()
        if not login:
            raise wtforms.ValidationError("账号或者密码错误")


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题字数超限")])
    content = wtforms.StringField(validators=[Length(min=3, message="格式错误")])
