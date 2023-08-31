import random
import datetime

from models import EmailCapture, UserModel
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, Flask, session
from exts import mail, db
from flask_mail import Message, Mail
from random import randint
from .forms import RegisterForm, LoginForm

bp = Blueprint('user', __name__)


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        login = LoginForm(request.form)
        if login.validate():
            user = UserModel.query.filter_by(email=login.email.data).first()
            session["email"] = login.email.data
            session["user_id"] = user.username
            session["id"] = user.id
            return redirect("/")
        else:
            return redirect(url_for("user.login"))


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            user_model = UserModel()
            user_model.username = form.username.data
            user_model.password = form.password.data
            user_model.email = form.email.data
            db.session.add(user_model)
            db.session.commit()
            email_capture = EmailCapture.query.filter_by(capture=form.captcha.data).first()
            db.session.delete(email_capture)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            print(form.errors)
            return redirect(url_for("user.register"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route("/captcha/email")
def captcha_email():
    email = request.args.get("email")
    if not email:
        return "请输入邮箱"
    code = randint(100000, 999999)
    msg = Message("验证码", sender="2728885797@qq.com", recipients=[email])
    msg.body = f"您的验证码是：{code}"
    mail.send(msg)
    EMAIL_CAPTCHA = EmailCapture(email=email, capture=code)
    EMAIL_CAPTCHA.date = datetime.datetime.now() + datetime.timedelta(minutes=10)
    db.session.add(EMAIL_CAPTCHA)
    db.session.commit()
    # msg_send = threading.Thread(target=mail.send(msg))
    # db_send = threading.Thread(target=db.session.commit())
    # db_add = threading.Thread(target=db.session.add(EMAIL_CAPTCHA))
    #
    # msg_send.start()
    # db_add.start()
    # db_send.start()

    # 给前端返回json格式
    return jsonify({"code": 200, "msg": "发送成功", "data": None})
