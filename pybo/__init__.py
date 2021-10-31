from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


#플라스크 애플리케이션을 생성하는 코드 '__name__'에는 모듈명이 담김 -> pybo.py라서 pybo
def create_app():
    app = Flask(__name__)
    # config.py의 내용을 app.config 환경변수로 부르기위해 아래코드¥추가
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    #블루프린트
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    #필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
