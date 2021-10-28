# redirect는 입력받은 Url로 리다이렉트 해주고 url_for은 라우트가 설정된 함수명으로 url을 역으로 찾아줌
from flask import Blueprint, url_for
from werkzeug.utils import redirect

# 블루프린트로 객체 생서시 이름, 모듈명, url프리픽스 값 정해줘¥
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return "Hello, Pybo!"


@bp.route('/')
def index():
    return redirect(url_for('question._list'))






