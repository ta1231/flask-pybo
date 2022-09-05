from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import config
from flaskext.markdown import Markdown

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # config.py 파일에 작성한 항목을 읽기 위해 추가

    # ORM
    db.init_app(app)
    # create_app 함수 안에서 init_app 메서드를 이용하여 app에 등록
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # 블루프린트 등록
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app


# 데이터베이스 관리 명령어 정리하기
'''
앞으로 모델을 추가하거나 변경할 때는 flask db migrate 명령과 flask db upgrade 명령만 사용할 것이다.
즉, 앞으로 데이터베이스 관리를 위해 여러분이 반드시 알아야 할 명령어는 다음 2가지이다.
flask db migrate: 모델을 새로 생성하거나 변경할 때 사용(실행하면 작업파일이 생성된다.)
flask db upgrate: 모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용(위에서 생성된 작업파일을 실행하여 데이터베이스를 변경한다.)
'''
