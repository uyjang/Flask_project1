from flask import Flask
from flask import render_template
from api_v1 import api as api_v1
from models import db, Fcuser
from flask_jwt import JWT
import os

# 플라스크를 설치할 때 템플릿을 다루는 패키지가 같이 설치 되어있음. (jinja라고 하는 것)
#app.py 는 장고에서 views.py와 같은 역할을 함

app = Flask(__name__)
app .register_blueprint(api_v1, url_prefix='/api/v1')
# 블루프린트는 내가 작성하는 컨트롤러코드들이 app.py에 모여있찌 않고 다른 곳으로 분리해서 작성할 수 있또록 하는 기능
# 그래서 컨트롤러 코드가 실제로는 api_v1에 있고 user.py에 있다

# html파일을 만들었으니 앱(컨트롤러)를 통해서 연결


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
def hello():
    return render_template('home.html')


basedir = os.path.abspath(os.path.dirname(__file__)) # 현재 있는 파일에 절대경로를 설정한다.
dbfile = os.path.join(basedir, 'db.sqlite')

# sqlahchemy는 orm(object relational mapper)라는 것으로 원래는 sql쿼리문이나 데이터베이스에서 지정한 방법으로 데이터를 불러오거나 관리하는데 이거는 객체형태로 파이썬 내부에서 사용할수 있게 해주는 것
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +  dbfile  # sqlalchemy에 필요한 설정값 넣어주기, uri를 통해 주소를 표시하는 것 / 현재 파일을 데이터베이스와 연동
# 티어다운은 사용자가 요청을 했을 때 원하는 정보를 줬을 때이고 그게 끝나면 커밋을 한다. 커밋이라는 동작을해야 쌓아진 동작을 데이터베이스에 작동하고 저장됨. 즉 실제 반영하는 느낌
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에대한 트랙을 하겠다라는 뜻인데 구버전에서 만든파일을 신버전으로 돌릴때 오류가 생길 시 트루로 바꾸면 됨
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECREY_KEY'] = 'kalfeinfqlkenf'


db.init_app(app)  # 위의 세가지 설정값 외에도 상당히 많은 설정값들이 있는데 그 값들을 초기화 해주는 코드
                  # 앱이 초기화가 됐으면
db.app = app      # 그 앱을 db안에 app이라는 곳에 넣음
db.create_all()  # 모델 클래스가 먼저 만들어져있고 그것을 생성한다는 것이니 모델클래스 작성이 완료되면 데이터베이스 파일을 생성함 


def authenticate(username, passwrod):
    user = Fcuser.query.filter(Fcuser.userid == username).first()
    if user.password == password:
        return user


def identity(payload):
    userid = payload['identity']  # 위에서 넣은 값들 중에서 id값이 아이덴티티값으로 들어가있다.
    return Fcuser.query.filter(Fcuser.id == userid).first()


# 인증해주는 기능하고 홈에서 페이로드가 넘어왔을 때 데이터를 반환해주는 기능까지 포함
jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

# pip install flask-sqlalchemy 는 모델을 만들기 전에 필요한 패키지
