from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')
"""
request 객체 : 플라스크에서 생성 과정 없이 사용할 수 있는 기본 객체, 
플라스크는 브라우저의 요청부터 응답까지의 처리구간에서 request객체를 사용할수 있게 해줌
"""


@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    question = Question.query.get_or_404(question_id)
    # <textarea name="content" id="content" rows="15"></textarea>에서 name이 content인걸 표시
    content = request.form['content']
    # answer의 경우 Answer(question=question, content=content, create_date=datetime.now())로 처리해도 괜춚
    answer = Answer(content=content, create_date=datetime.now())
    question.answer_set.append(answer) # db.session.add(answer)로 대체 가능
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
