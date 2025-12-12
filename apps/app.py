from pathlib import Path  # p100

from flask import Flask
from flask_migrate import Migrate  # p100
from flask_sqlalchemy import SQLAlchemy  # p100
from flask_wtf import CSRFProtect  # p117

db = SQLAlchemy()  # ORM객체 생성
csrf = CSRFProtect()  # p117


def create_app():
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # db용 코드 추가 p100
    # 앱의 config 설정을 한다.
    app.config.from_mapping(
        SECRET_KEY="12345678901234567890",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MEDIFICATIONS=False,
        # SQL을 콘솔 로그에 출력하는 설정
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY="12345678901234567890",
    )

    # csrf 함수를 앱에 연결한다. p117
    csrf.init_app(app)
    # apps/crud/forms.py 파일을 생성하여 작업한다.

    # SQLAlchemy와 앱을 연결한다.
    db.init_app(app)

    # Migrate와 앱을 연결한다.
    Migrate(app, db)

    # apps/crud/models.py를 만들고 데이터베이스 조작용 코드를 기입힌다.

    from apps.crud import views as crud_views

    # crud 패키지로 부터 views를 impoort 한다.

    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    # 블루프린터라 불리는 기능인 app.register_blueprint 함수를 이용해 crud앱을 등록함
    # url_prefix에 /crud를 지정하고, 이 views의 엔드포인트의 모든 url이 crud로 부터 시작 되게 한다.

    # Blueprint란
    # 앱을 분할 하기 위한 플라스크의 기능
    # 앱의 규모가 커저도 간경한 상태를 유지할 수 있어 보수성이 향상됨

    # 1. 앱을 분할 할 수 있다.
    # 2. url 프리픽스 및 서브 도메인을 지정하여 다른 애플리케이션 루트와 구별할 수 있다.
    # 3. Blueprint 단위로 템플릿을 나눌 수 있다.
    # 4. Blueprint 단위로 정적파일을 나눌 수 있다.

    # Blueprint를 이용하려면 Blueprint 객체(Blueprint 앱)을 생성하고,
    # 플라스크 앱인 app 인스턴스의 register_blueprint 메서드를 전달해 등록한다.

    # 플라스크 앱              플라스크앱에 등록
    # CRUD앱 /crud            register_blueprint(Blueprint(CRUD 앱 : 템플릿, 정적파일))
    # 인증앱 /auth            register_blueprint(Blueprint(인증 앱 : 템플릿, 정적파일))
    # 물체감지앱 /            register_blueprint(Blueprint(물체감지 앱 : 템플릿, 정적파일))

    # Blueprint 클래스의 주요 생성자
    # name : Blueprint 앱의 이름, 각 엔드포인트명 앞에 추가됨
    # import_name : Blueprint 앱의 패키지(apps, curd, views)의 이름, 보통 __name__을 지정한다.
    # static_folder : Blueprint 앱의 정적 파일용 폴더, 디폴트로는 무효
    # template_folder : Blueprint 앱의 템플릿 파일용 디렉토리, 디폴트로는 무효
    #                   Blueprint의 템플릿은 앱 본체의 템플릿 디렉토리보다 우선순위가 낮다.
    # url_prefix : Blueprint 앱의 모든 URL 맨 앞에 추가하여 다른 앱의 경로와 구별하기 위한 경로
    # subdomain : Blueprint를 서브 도메인으로서 이용하는 경우 지정

    # Blueprint 객체 생성 예제
    # template_folder와 static_folder를 지정하지 않은 경우는
    # Blueprint 앱용 템플릿과 정적파일을 이용할 수 없다.

    # sample = Blueprint(
    #     __name__,
    #     "sample",
    #     static_folder="static"
    #     template_folder="template",
    #     url_prefix="/sample"
    #     subdomain="example",
    # )
    # 생성한 sample 객체는 register_blueprint 함수로 등록한다.
    # app.register_blueprint(sample, url_prefix="/sample", subdomain="example")
    # app.register_blueprint의 대표적인 인수
    # blueprint : 등록하는 Blueprint앱 뒤에서 설명하는 Blueprint 클래스의 객체를 지정
    # url_prefix : 모든 URL의 맨앞에 추가하는 다른 앱의 경로와 구별하기 위한 경로
    # subdomain : 서브도메인으로 이용하는 경우 작성

    # app.register_blueprint와 Blueprint 클래스에서 지정하는 파라미터가 중복하는 경우
    # app.register_blueprint의 값이 우선해서 이용된다.

    # Blueprint로 앱을 분할 하는 모듈화
    # Blueprint로 앱을 얼마나 잘게 분할 할지에 대한 정해진 규칙은 없다.
    # 만들고 싶은 앱에 적합하게 모듈화해 분할 하는 것이 이상적이지만, 2개의 기준으로서 기능을 나눈다.
    # 1. url 프리픽스 및 서브 도메인을 나누고 싶은가?
    # 2. 화면의 레이아웃으로 나누고 싶은가?
    # 예를 들면 토털사이트의 뉴스, 카페, 블로그, 쇼핑, 지도 등....

    # 여러개의 Blueprint로 템플릿을 이용할 때 주의사항
    # Blueprint로 등록한 앱의 템플릿을 이용하는 경우 Blueprint의 생성자에 template_folder 파라미터로 지정
    # crud = Blueprint("crud", __name__, template_folder="templates" )
    # 다만 여러개의 Blueprint가 똑같이 상대 템플릿 경로를 이용하는 경우 가장 먼저 등록한 Blueprint의
    # 템플릿이 다른 Blueprint의 템플릿보다 우선되면 2번째 이후의 Blueprint 템플릿을 표사할 수 없게 된다.
    # 이를 방자하려면 templates 디렉토리와 html 파일 사이에 Blueprint로 등록한 앱이름의 디렉토리를 끼워야 한다.
    # apps
    # ---app.py
    # ---auth (Blueprint)
    # ------templates
    # ---------auth (사이에 끼운다.)
    # ------------base.html
    # ------------index.html
    # ------------login.html
    # ------------signup.html

    # 환경변수 변경 .env
    # minimalapp의 app은 apps/minimalapp/app.py에 있는데
    # crud앱은 apps/app.py의 create_app 함수에서 생성함으로
    # FLASK_APP=apps.app:create_app 으로 변경한다.
    # 함수로 앱을 생성하는 경우 모듈:함수와 같이 지정한다.
    # 또한 앱을 생성하는 함수명이 create_app의 경우는 자동으로 create_app 함수를 호출함으로
    # apps.app.py로 지정 가능함

    return app


# P99
# SQLAlchemy란 파이썬이 제공하는 ORM(Object-Relational Mapping)이다.
# O/R 매퍼는 데이터베이스와 프로그래밍 언어 간에 호환되지 않는 데이터를 변환한다.
# SQLAlchemy를 이용하면 SQL 코드를 쓰지 않고 파이썬 코드로 데이터베이스의 CRUD를 한다.
# 확장 기능 설치
# pip install flask-sqlalchemy ORM용 추가
# pip install flask-migrate    데이터베이스 마이크레이션하는 확장 기능
# 마이그레이션은 코드 정보를 바탕으로 데이터베이스의 테이블 작성이나 컬럼 변경등을 하는 기능
# 코드를 바탕으로 SQL이 발행되며, SQL 정보를 파일로 유지하기 위해 계속적으로 데이터베이스의 갱신이나 롤백이 가능

# SQLite는 데이터베이스 서버를 준비하지 않아도 됨 (앱에 내장해서 이용하는 오픈소스)
# 로컬에 데이터를 파일로 저장할 수 있다.
# 상단에 from 추가
# from pathlib import Path
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy


# p116 폼의 확장기능 이용하기
# flask-wtf는 유효성 검증이나 CSRF에 대처하기 위한 폼을 작성하는 플라스크의 확장
# 장점 : HTML을 쉽고 간편하게 작성, 폼의 유효성 검증, CSRF에 대처 가능
# pip install flask-wtf
