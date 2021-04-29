from flask import Blueprint
# init안에 api에서 제공하는 파일을 연결시켜야 다른 데서 api를 가져갈 수 있다.

api = Blueprint('api', __name__)


from . import user