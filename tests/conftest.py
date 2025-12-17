# pytest의 전처리 공통 모듈 화 (공유 처리)
# 픽스처는 개개의 테스트 파일에서 사용할 수 있는데
# 여러개의 테스트 파일에서 픽스처를 공유하려면 conftest.py를 테스트 파일과 함께 배치 한다.
# tests 패키지 아래에 conftest.py를 작성하고 픽스처를 적성하면 tests 패키지 아래의 모든 테스트에서 픽스처를 사용함

import pytest


@pytest.fixture  # 픽스처를 추가한다.
def app_data():
    print("픽스처를 이용한 전처리")
    return 3
    # pytest test_sample.py::test_func3
    # ============================== test session starts ================================
    # platform win32 -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0
    # rootdir: C:\flaskbook\tests
    # collected 1 item
    #
    # test_sample.py .                                                                                                                                              [100%]
    #
    # ============================== 1 passed in 0.01s ===================================
    # (venv) PS C:\flaskbook\tests>
    # 공통 모듈 처리 완료


# p 264 추가
# 이미 작성한 tests/conftest.py는 tests/detector 패키지를 사용할 수 있다.
# conftest.py의 픽스처를 갱신하고 물체감지 앱의 테스트를 할 수 있도록 설정 처리와 클린업(db) 처리를 추가한다.
# 설정 처리에서는 앱을 작성하고 데이터베이스를 초기화 한다.
# 이제부터 작성하는 앱의 테스트함수는 yield(생산하다, 수확하다)를 사용하여 실행한다.
# yield가 포함되어 있는 경우는 여기에서 테스트가 실행된다.
# 테스트가 종료되면 yield 다음 행의 픽스처 함수의 처리가 실행 됨
# 클린업 처리에서는 테스트 실행 후 작성된 데이터베이스를 클리어 한다.
# 이런 처리는 테스트 함수별로 실행됨

import os
import shutil  # shell utilities 모듈은 파일을 복사하거나 이동하는 등의 파일 관리 작업을 위한 고수준의 파일 연산을 제공합니다

from apps.app import create_app, db
from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag


# 픽스처 함수를 작성한다.
@pytest.fixture
def fixture_app():
    # 설정 처리
    # 테스트용 config()를 사용하기 위해서 인수에 testing를 지정한다.
    app = create_app("testing")

    # 데이터베이스를 이용하기 위한 선언을 한다.
    app.app_context().push()

    # 테스트용 데이터베이스의 테이블의 작성한다.
    with app.app_context():
        db.create_all()

    # 테스트용의 이미지 업로드 디렉토리를 작성한다.
    os.mkdir(app.config["UPLOAD_FOLDER"])

    # 테스트를 실행한다.
    yield app

    # 클린업 처리
    # user 테이블의 레코드를 삭제한다.
    User.query.delete()

    # user_image 테이블의 레코드를 삭제한다.
    UserImage.query.delete()

    # user_image_tags 테이블의 레코드를 삭제한다.
    UserImageTag.query.delete()

    # 테스트용 이미지 업로드 디렉토리를 삭제한다.
    shutil.rmtree(app.config["UPLOAD_FOLDER"])

    db.session.commit()


# Flask의 테스트 클라이언트를 반환하는 픽스처 함수를 작성한다.
@pytest.fixture
def client(fixture_app):
    # Flask의 테스트용 클라이언트를 반환한다.
    return fixture_app.test_client()
