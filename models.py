from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # 1.


class Fcuser(db.Model):  # 2.모델클래스
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))

    @property  # 밑에 함수가와도 변수처럼 사용되게 하는 코드
    def serialize(self):
        return {
            'id': self.id,
            'password': self.password,
            'userid': self.userid,
            'username': self.username
        }
