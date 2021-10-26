from flask import Flask

#플라스크 애플리케이션을 생성하는 코드 '__name__'에는 모듈명이 담김 -> pybo.py라서 pybo
app = Flask(__name__)


#특정 url접근시 바로 다음줄에 있는 함수를 호출하는 데코레이트
@app.route('/')
def hello_pybo():
    return 'Hello, pybo!'
