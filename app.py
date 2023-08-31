from flask import Flask, session, g, render_template
import config
from exts import db, mail
from models import UserModel
from blueprints.user import bp as user_bp
from blueprints.answer import bp as answer_bp
from flask_migrate import Migrate
from models import UserModel, EmailCapture, QuestionModel

app = Flask(__name__)
migrate = Migrate(app, db)

# 绑定配置
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(answer_bp)


@app.before_request
def my_before_request():  # put application's code here
    user_id = session.get("user_id")
    email = session.get("email")
    id = session.get("id")
    if user_id:
        setattr(g, "user_id", user_id)
        setattr(g, "email", email)
        setattr(g, "id", id)
    else:
        setattr(g, "user_id", None)
        setattr(g, "email", None)
        setattr(g, "id", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user_id}


@app.route("/")
def index():
    return render_template("base.html")


if __name__ == '__main__':
    app.run()
