from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


# POST 방식 요청에는 로그인을 수행하고, GET 방식 요청에는 로그인 템플릿을 렌더링한다.
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다')
    # form 태그에 action 속성이 지정되지 않은 경우, POST 방식으로 /auth/signup/ 이 호출되게 된다.
    return render_template('auth/signup.html', form=form)


# POST 방식 요청에는 로그인을 수행하고, GET 방식 요청에는 로그인 템플릿을 렌더링한다.
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다"
        if error is None:
            """
            세션은 request와 마찬가지로 플라스크가 자동으로 생성하여 제공하는 변수이다.
            쉽게 말해 세션은 플라스크 서버를 구동하는 동안에는 영구히 참조할 수 있는 값이다.
            session 변수에 user의 id값을 저장했으므로 다양한 URL 요청에 이 세션값을 사용할 수 있다. 
            예를들어 현재 웹 브라우저를 요청한 주체가 로그인한 사용자인지 아닌지를 판별할 수 있다.
            """
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.before_app_request
# 이 애너테이션이 적용된 함수는 라우트 함수보다 먼저 실행된다.
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # g.user에는 User 객체가 저장된다.
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
