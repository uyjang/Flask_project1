from flask import jsonify
# view코드를 만드는 곳(app이랑 비슷)
from . import api  # 이닛 안에 있는 api
from flask import request
from models import Fcuser, db
from flask_jwt import jwt_required  # 데코레이터가 들어있는 곳


@api.route('/users', methods=['GET', 'POST'])
# GET은 데이터에대한 조회, POST는 생성
# 여기서 쓰는 api는 __init__.py에서 api = Blueprint('api', __name__)이라는 변수에 설정해 놓은 것에서 가져왔다.
@jwt_required()
def users():
    if request.method == 'POST':
        # html에서 폼형식으로 받을 때는 아래의 코드처럼 데이터를 가져왔지만 json형태로 바뀌면서 data형태로 가져와야됨
        # userid = request.form.get(('userid'))
        # username = request.form.get(('username'))
        # password = request.form.get(('password'))
        # re-password = request.form.get(('re-password'))
        data = request.get_json()
        userid = data.get('userid')
        username = data.get('username')
        password = data.get('password')
        re_password = data.get('re-password')

        if not (userid and username and password and re_password):
            return jsonify({'error': 'No arguments'}), 400
        if password != re_password:
            return jsonify({'error': 'Wrong password'}), 400

        fcuser = Fcuser()
        fcuser.userid = userid
        fcuser.username = username
        fcuser.password = password

        db.session.add(fcuser)  # db안에 위에서 넣은 데이터들을 넣겠다.
        db.session.commit()  # 커밋까지 해야 완료

        return jsonify(), 201  # 템플릿으로 렌더한 것이 아니라 json의 리소스만 반환해줌 / 즉, 응답으로 성공여부와 데이터만 전달

    users = Fcuser.query.all()
    # GET요청으로 모든 사용자 리스트를 불러오기 위한 코드 시작
    # Fcuser는 클래스모델이고 클래스는 json형식처럼 문자열로 표현하기(시리얼라이저블)가 쉽지않음. 고로 models파일 안에 직렬화하는 변수를 넣는다

    # rest로 진행할 때는 html을 반환하는게 아니라 json타입의 데이터를 반환
    return jsonify([users.serialize for user in users])
    # 지능형 리스트


@api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
# 해당 id의 유저를 조회하면서 조회,수정,삭제가 가능하도록 메소드를 줌
def user_detail(uid):  # uid가 함수의 인자값으로 들어옴
    if request.method == 'GET':
        # 필터는 조건에 맞는 여러개의 데이터를 뽑아내기때문에 first를 통해서 하나만 가져온다는 뜻
        user = Fcuser.query.filter(Fcuser.id == uid).first()
        return jsonify(user.serialize)  # 유저는 클래스변수라서 시리얼라이즈를 해줘야 한다.
    elif request.method == 'DELETE':
        Fcuser.query.delete(Fcuser.id == uid)
        return jsonify(), 204  # 콘텐츠가 안들어있음을 나타내는 코드를 보여줌

    data = request.get_json()
    # post요청일 때는 폼을 통해 데이터들을 가져왔지만 제이손은 위의 코드를 통해 데이터를 가져온다

    userid = data.get(('userid'))
    username = data.get(('username'))
    password = data.get(('password'))

    updated_data = {}  # 위에서 데이터가 없을 경우엔 빈곳에  아무것도 안들어가서 빈곳이 유지가 돼서 프로그램에 이상이 없음. 그래서 비워놓은 거임
    if userid:
        updated_data['userid'] = userid
    if username:
        updated_data['username'] = username
    if password:
        updated_data['password'] = password

    Fcuser.query.filter(Fcuser.id == uid).update(updated_data)
    # 업데이트가 됐으니 다시 데이터를 가져온다
    user = Fcuser.query.filter(Fcuser.id == uid).first()
    return jsonify(user.serialize)
