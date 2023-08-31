import datetime

from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g
from .forms import QuestionForm
from models import QuestionModel
from exts import db
from datetime import datetime

bp = Blueprint('answer', __name__, url_prefix="/")


@bp.route("/answer/public", methods=["GET", "POST"])
def public_ans():
    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            author_id = g.get("id")
            question = QuestionModel(title=title, context=content, author_id=author_id)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect("/")
