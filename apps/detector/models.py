# UserImage 모델은 로그인한 사용자가 이미지를 업로드 했을 때 이미지 URL을 저장하기 위한 모델
# user테이블의 id를 user_images 테이블의 user_id로 릴레이션을 적용 (pk_fk)
# 사용자는 몇번이고 이미지를 업로드할 수 있음으로 1대 다 관계

from datetime import datetime

from apps.app import db


class UserImage(db.Model):
    __tablename__ = "user_images"
    id = db.Column(db.Integer, primary_key=True)
    # user_id는 users 테이블의 id 컬럼을 외부 키로서 설정한다
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    image_path = db.Column(db.String)
    is_detected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# flask db migrate
# flask db upgrade

#
# CREATE TABLE user_images (
#         id INTEGER NOT NULL,
#         user_id VARCHAR,
#         image_path VARCHAR,
#         is_detected BOOLEAN,
#         created_at DATETIME,
#         updated_at DATETIME,
#         PRIMARY KEY (id),
#         FOREIGN KEY(user_id) REFERENCES users (id)
# )


# flask shell을 이용하면 sql을 테스트 할 수 있다.
# 사전준비
# 콘솔(터미널)
# flask shell
# from apps.app import db
# from apps.crud.models import User
# from apps.detector.models import UserImage

# INNER JOIN(내부 결합)
# 양쪽 테이블에 모두 존재하는 데이터를 추출하는 결합 방법
# join을 사용해 filter에 User.id == UserImage.user_id를 지정
# 취득하는 데이터는 User와 UserImage의 모든 칼럼을 대상으로 함
# query 인수에 User 클래스와 UserImage 클래스를 지정함
# 콘솔(터미널)
# db.session.query(User, UserImage).join(UserImage).filter(User.id == UserImage.user_id).all()
#                  클래스들              fk 설정한곳에 모든~         동등비교

# SELECT users.id AS users_id, users.username AS users_username, users.email AS users_email, users.password_hash AS users_password_hash,
# users.created_at AS users_created_at, users.updated_at AS users_updated_at,
# user_images.id AS user_images_id, user_images.user_id AS user_images_user_id, user_images.image_path AS user_images_image_path,
# user_images.is_detected AS user_images_is_detected, user_images.created_at AS user_images_created_at,
# user_images.updated_at AS user_images_updated_at
# FROM users JOIN user_images ON users.id = user_images.user_id
# WHERE users.id = user_images.user_id (0.00052초)
# 위 방법 보다 간단한 방법

# 외부키가 설정 되어 있음으로 아래와 같이 설정해야 한다.
# db.session.query(User, UserImage).join(UserImage).all()  필터부분 제외
# SELECT users.id AS users_id, users.username AS users_username, users.email AS users_email, users.password_hash AS users_password_hash,
# users.created_at AS users_created_at, users.updated_at AS users_updated_at,
# user_images.id AS user_images_id, user_images.user_id AS user_images_user_id, user_images.image_path AS user_images_image_path,
# user_images.is_detected AS user_images_is_detected, user_images.created_at AS user_images_created_at,
# user_images.updated_at AS user_images_updated_at
# FROM users JOIN user_images ON users.id = user_images.user_id
# where문이 사라진다.  (0.00045초)

# OUTER JOIN(외부 결합)
# 은 기준이 되는 테이블에 존재하면(다른 쪽의 테이블에 없어도) 데이터를 추출하는 결합 방법
# outerjoin을 사용하여 filter에 User.id = UserImage.user_id를 지정하여 결합
# db.session.query(User, UserImage).outerjoin(UserImage).filter(User.id == UserImage.user_id).all()
# SELECT users.id AS users_id, users.username AS users_username, users.email AS users_email, users.password_hash AS users_password_hash,
# users.created_at AS users_created_at, users.updated_at AS users_updated_at,
# user_images.id AS user_images_id, user_images.user_id AS user_images_user_id, user_images.image_path AS user_images_image_path,
# user_images.is_detected AS user_images_is_detected, user_images.created_at AS user_images_created_at,
# user_images.updated_at AS user_images_updated_at
# FROM users LEFT OUTER JOIN user_images ON users.id = user_images.user_id
# WHERE users.id = user_images.user_id (0.00053초)

# 릴레이션십
# https://docs.sqlalchemy.org/en/14/orm/backref.html
# 모델에 릴레이션십을 지정함으로 써 모들 객체로부터 관련한 테이블의 객체를 추출할 수 있다.
# user테이블과 userimage 테이블 관계의 경우 user_images 테이블에는 외부키를 정의하고
# user 테이블에 릴레이션십을 정의한다.
# >>> user_images = relationshil("UserImage")
# 주요 옵션
# backref : 다른 모델에 대해서 양방향으로 릴레이션 한다.
# lazy : 지연로딩으로 기본값은 select이며 다른 옵션에는 immediate, joined, subquery, noload, dynamic 등이 있다.
# order_by : 정렬용
# https://databoom.tistory.com/entry/FastAPI-SQLAlchemy-%EC%83%81%EC%84%B8-ForeignKey-relationship-6-5

# backref를 이용하면 User 모델로부터 UserImage 모델로, 그 반대도 사용하여 접근할 수 있다.
# 테이블 관계는 1:1, 1:n , n:1 대해서는 가능하지만 n:m 테이블에 대해서는 이용할 수 없다.
# n:m 테이블에 대해서는 secondary나 secondaryjoin을 이용한다.
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#using-a-late-evaluated-form-for-the-secondary-argument

# User 객체로부터 UserImage 객체 가져오기
# 객체를 가져오려면 user.user_images와 같이 작성한다.
# 이 경우, User 객체의 user_id를 가진 UserImage 정보를 취득할 수 있다.
# backref의 디폴트 값은 select로 되어 있으며, user.user_images가 호출 되었을 시에 한번만 sql이 실행된다.
# 1:n 관계에 있으므로 user.user_images로 취득할 수 있는 값은 UserImage 객체의 리스트임

# 콘솔(터미널) 종료 후 User객체를 변경한다.
# crud/models.py에 User 함수에 user_images = db.relationship("UserImage", backref="user") 추가
# 콘솔(터미널) flask shell
# from apps.app import db
# from apps.crud.models import User
# from apps.detector.models import UserImage

# User 객체로 부터 UserImage 객체를 취득
# user = User.query.first() users 테이블로부터 레코드를 취득한다.
# SELECT users.id AS users_id, users.username AS users_username, users.email AS users_email, users.password_hash AS users_password_hash,
# users.created_at AS users_created_at, users.updated_at AS users_updated_at
# FROM users
# LIMIT ? OFFSET ?

# print(user.user_images) 테스트 (user_images) 테이블로부터 user_id를 보유하는 레코드를 취득한다.
# SELECT user_images.id AS user_images_id, user_images.user_id AS user_images_user_id, user_images.image_path AS user_images_image_path,
# user_images.is_detected AS user_images_is_detected, user_images.created_at AS user_images_created_at,
# user_images.updated_at AS user_images_updated_at
# FROM user_images
# WHERE ? = user_images.user_id (user_images 테이블로부터 user_id)를 보유하는 레코드를 취득한다.


# UserImage 객체로부터 User 객체 취득하기
# user_image.user와 같이 기술하면 가능
# 이경우 UserImage 객체의 user_id를 가진 User 정보를 취득할 수 있다.
# n:1 의 관계에 있으므로 User는 리스트가 아닌 객체가 된다.
# 다음 결과를 출력하려면 User_images 테이블에 users테이블의 user_id를 유지하는 레코드가 있어야 한다.

# user_image = UserImage.query.first()
# SELECT user_images.id AS user_images_id, user_images.user_id AS user_images_user_id,
# user_images.image_path AS user_images_image_path, user_images.is_detected AS user_images_is_detected,
# user_images.created_at AS user_images_created_at, user_images.updated_at AS user_images_updated_at
# FROM user_images
# LIMIT ? OFFSET ?

# print(user_image.user) db에 아직 정보가 없어서 안나온다.
# exit() 로 종료

# order_by를 사용하면 정렬하여 출력된다.
# crud/models.py에 정렬 설정 추가
# 콘솔(터미널) flask shell
# from apps.app import db
# from apps.crud.models import User
# from apps.detector.models import UserImage

# user = User.query.first()
# print(user.user_images)
# SELECT user_images.id AS user_images_id, user_images.user_id AS user_images_user_id, user_images.image_path AS user_images_image_path,
# user_images.is_detected AS user_images_is_detected, user_images.created_at AS user_images_created_at,
# user_images.updated_at AS user_images_updated_at
# FROM user_images
# WHERE ? = user_images.user_id ORDER BY user_images.id DESC
#                               정렬 구문이 추가 된다.


# p219 물체 감지 테이블 생성
class UserImageTag(db.Model):
    # 테이블명을 지정한다
    __tablename__ = "user_image_tags"
    id = db.Column(db.Integer, primary_key=True)
    # user_image_id는 user_images 테이블의 id 컬럼의 외부로서 설정한다
    user_image_id = db.Column(db.String, db.ForeignKey("user_images.id"))
    tag_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# flask db migrate
# flask db upgrade
# CREATE TABLE user_image_tags (
#         id INTEGER NOT NULL,
#         user_image_id VARCHAR,
#         tag_name VARCHAR,
#         created_at DATETIME,
#         updated_at DATETIME,
#         PRIMARY KEY (id),
#         FOREIGN KEY(user_image_id) REFERENCES user_images (id)
# )
