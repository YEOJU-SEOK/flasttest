import os


BASE_DIR = os.path.dirname(__file__)

#DB접속주소
SQLALCHEMY_DATABASE_URL = 'squlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
#sqlalchemy의 이벤트를 처리하는 옵션(필요하진 않아서 False)
SQLALCHEMY_TRACK_MODIFICATIONS = False
