from flask import Blueprint

#블루프린트로 객체 생서시 이름, 모듈명, url프리픽스 값 정해줘¥
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return "Hello, Pybo!"


@bp.route('/')
def index():
    return "Pybo index"
