# flask routes 명령어로 경로 정보를 확인한 후 detector로 시작하는 엔드포인트를
# 테스트 대상으로 만들자

# detector.delete_image  POST       /images/delete/<string:image_id> 이미지 삭제
# detector.detect        POST       /detect/<string:image_id>  이미지 객체
# detector.image_file    GET        /images/<path:filename> 이미지 파일
# detector.index         GET        /   이미지 리스트
# detector.search        GET        /images/search 태그 이미지 검색
# detector.upload_image  GET, POST  /upload 이미지 업로드 화면

# p267 추가
# 이미지 일람 화면의 테스트를 작성한다.
# 이미지 일람 화면은 미로그인 상태와 로그인 상태 모두 접속할 수 있으므로
# 미로그인 상태와 로그인상태의 표시 확인 한다.


# 로그인을 하지 않았을 때 (미 로그인 상태에서는 로그인, 이미지 신규 등록이라는 문자열을 확인)
def test_index(client):
    rv = client.get("/")  # http://localhost:5000/
    assert "로그인" in rv.data.decode()
    # 결과가 html로 저장되어 있으므로 로그인과
    assert "이미지 신규 등록" in rv.data.decode()
    # 이미지 신규 등록이라는 문자열이 있는 것을 확인한다.
    # 결과가 바이트 타입으로 변환됨으로 decode() 메서드로 디코드 한다.


# 로그인을 했을 경우
# 1. 회원가입을 먼저하고 테스트하는 방법을 처리해보자.
# 2. 회원가입 후에 로그인을 진행하고 로그아웃, 이미지 신규 등록이라는 문자열을 확인
def signup(client, username, email, password):
    """회원가입한다."""
    data = dict(username=username, email=email, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)
    #                                            회원가입후 지정경로로 이동하는 값 활성화


def test_index_signup(client):
    """회원가입을 실행한다."""
    rv = signup(client, "admin", "kkw@kkw.com", "kkw")
    assert "admin" in rv.data.decode()

    rv = client.get("/")
    assert "로그아웃" in rv.data.decode()
    assert "이미지 신규 등록" in rv.data.decode()

    # pytest -v -s 로 테스트

    # (venv) PS C:\flaskbook\tests> pytest -v -s
    # =================== test session starts ======================================================
    # platform win32 -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0 -- C:\flaskbook\venv\Scripts\python.exe
    # cachedir: .pytest_cache
    # rootdir: C:\flaskbook\tests
    # collected 5 items
    #
    # detector/test_views.py::test_index PASSED
    # detector/test_views.py::test_index_signup PASSED
    # test_sample.py::test_func1 PASSED
    # test_sample.py::test_func2 FAILED
    # test_sample.py::test_func3 픽스처를 이용한 전처리
    # PASSED
    #
    # ======================== FAILURES =============================================================
    # ______________________ test_func2 ____________________________________________________________
    #
    # def test_func2():
    # >       assert 1 == 2
    # E       assert 1 == 2
    #
    # test_sample.py:54: AssertionError
    # ================ short test summary info =====================================================
    # FAILED test_sample.py::test_func2 - assert 1 == 2
    # ==================================


# 이미지 업로드 화면 테스트 p268
def test_upload_no_auth(client):
    rv = client.get("/upload", follow_redirects=True)
    # 이미지 업로드 화면에는 접근할 수 없다
    assert "업로드" not in rv.data.decode()
    # 로그인 화면으로 리다이렉트된다
    assert "메일 주소" in rv.data.decode()
    assert "비밀번호" in rv.data.decode()


# 로그인 했을 경우
def test_upload_signup_get(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = client.get("/upload")
    assert "업로드" in rv.data.decode()


# 유효성 검증 오류가 발생하면
from pathlib import Path  # p269 추가

from flask.helpers import get_root_path  # p269 추가
from werkzeug.datastructures import FileStorage  # p269 추가

from apps.detector.models import UserImage  # 269 추가


def upload_image(client, image_path):
    """이미지를 업로드한다"""
    image = Path(get_root_path("tests"), image_path)
    test_file = (
        FileStorage(
            stream=open(image, "rb"),
            filename=Path(image_path).name,
            content_type="multipart/form-data",
        ),
    )
    data = dict(
        image=test_file,
    )
    return client.post("/upload", data=data, follow_redirects=True)


# detector/testdata 디렉토리 생성
def test_upload_signup_post_validate(client):
    signup(client, "admin", "kkw@kkw.com", "kkw")
    rv = upload_image(client, "detector/testdata/test_invalid_file.txt")
    assert "지원되지 않는 이미지 형식입니다." in rv.data.decode()


def test_upload_signup_post(client):
    signup(client, "admin", "kkw@kkw.com", "kkw")
    rv = upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()


def test_detect_no_user_image(client):
    signup(client, "admin", "kkw@kkw.com", "kkw")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    # 존재하지 않는 ID를 지정한다
    rv = client.post("/detect/notexistid", follow_redirects=True)
    assert "물체 대상의 이미지가 존재하지 않습니다." in rv.data.decode()


# 물체 감지에 성공할 때
def test_detect(client):
    # 사인업한다
    signup(client, "admin", "kkw@kkw.com", "kkw")

    # 이미지를 업로드한다
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()

    # 물체 검지를 실행한다
    rv = client.post(f"/detect/{user_image.id}", follow_redirects=True)
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()
    assert "dog" in rv.data.decode()


# 태그를 검색할 때
def test_detect_search(client):
    # 사인업한다
    signup(client, "admin", "kkw@kkw.com", "kkw")

    # 이미지를 업로드한다
    upload_image(client, "detector/testdata/test_valid_image.jpg")

    user_image = UserImage.query.first()
    # 물체 검지한다
    client.post(f"/detect/{user_image.id}", follow_redirects=True)

    # dog 워드로 검색한다
    rv = client.get("/images/search?search=dog")

    # dog 태그의 이미지가 있는 것을 확인한다
    assert user_image.image_path in rv.data.decode()

    # dog 태그가 있는 것을 확인한다
    assert "dog" in rv.data.decode()

    # test 워드로 검색한다
    rv = client.get("/images/search?search=test")

    # dog 태그의 이미지가 없는 것을 확인한다
    assert user_image.image_path not in rv.data.decode()

    # dog 태그가 없는 것을 확인한다
    assert "dog" not in rv.data.decode()


# 삭제 버튼을 클릭했을 때 테스트
def test_delete(client):
    signup(client, "admin", "kkw@kkw.com", "kkw")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()
    image_path = user_image.image_path
    rv = client.post(f"/images/delete/{user_image.id}", follow_redirects=True)
    assert image_path not in rv.data.decode()


# 커스텀 오류 화면 테스트용
def test_custom_error(client):
    rv = client.get("/notfound")
    assert "404 Not Found" in rv.data.decode()


# 최종 결과
# (venv) PS C:\flaskbook\tests> pytest -v -s
# ======================================================= test session starts =======================================================
# platform win32 -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0 -- C:\flaskbook\venv\Scripts\python.exe
# cachedir: .pytest_cache
# rootdir: C:\flaskbook\tests
# collected 14 items

# detector/test_views.py::test_index PASSED
# detector/test_views.py::test_index_signup PASSED
# detector/test_views.py::test_upload_no_auth PASSED
# detector/test_views.py::test_upload_signup_get PASSED
# detector/test_views.py::test_upload_signup_post_validate PASSED
# detector/test_views.py::test_upload_signup_post PASSED
# detector/test_views.py::test_detect_no_user_image PASSED
# detector/test_views.py::test_detect tensor(0.9967, grad_fn=<UnbindBackward0>)
# dog
# tensor(0.9938, grad_fn=<UnbindBackward0>)
# bicycle
# tensor(0.7150, grad_fn=<UnbindBackward0>)
# potted plant
# tensor(0.6565, grad_fn=<UnbindBackward0>)
# car
# tensor(0.5940, grad_fn=<UnbindBackward0>)
# truck
# PASSED
# detector/test_views.py::test_detect_search tensor(0.9967, grad_fn=<UnbindBackward0>)
# dog
# tensor(0.9938, grad_fn=<UnbindBackward0>)
# bicycle
# tensor(0.7150, grad_fn=<UnbindBackward0>)
# potted plant
# tensor(0.6565, grad_fn=<UnbindBackward0>)
# car
# tensor(0.5940, grad_fn=<UnbindBackward0>)
# truck
# PASSED
# detector/test_views.py::test_delete PASSED
# detector/test_views.py::test_custom_error PASSED
# test_sample.py::test_func1 PASSED
# test_sample.py::test_func2 FAILED
# test_sample.py::test_func3 픽스처를 이용한 전처리
# PASSED

# ============================================================ FAILURES =============================================================
# ___________________________________________________________ test_func2 ____________________________________________________________

#     def test_func2():
# >       assert 1 == 2
# E       assert 1 == 2

# test_sample.py:54: AssertionError
# ===================================================== short test summary info =====================================================
# FAILED test_sample.py::test_func2 - assert 1 == 2
# ================================================== 1 failed, 13 passed in 15.69s ==================================================
# (venv) PS C:\flaskbook\tests>


# p273 테스트 커버리지 출력하기
# 테스트의 커버리지는 앱의 코드에 대해 테스트 코드가 얼마나 실행 되었는지를 비율로 나타낸다.
# pip install pytest-cov 로 설치한다.

# pytest detector --cov=../apps/detector

# (venv) PS C:\flaskbook\tests> pytest detector --cov=../apps/detector
# ======================================================= test session starts =======================================================
# platform win32 -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0
# rootdir: C:\flaskbook\tests
# plugins: cov-7.0.0
# collected 11 items
#
# detector\test_views.py ...........                                                 [100%]
#
# ================================== tests coverage ========================================
# _________________ coverage: platform win32, python 3.11.2-final-0 __________________________
#
# Name                                     Stmts   Miss  Cover
# ------------------------------------------------------------
# C:\flaskbook\apps\detector\__init__.py       1      0   100%
# C:\flaskbook\apps\detector\forms.py         10      0   100%
# C:\flaskbook\apps\detector\models.py        17      0   100%
# C:\flaskbook\apps\detector\views.py        145     12    92%
# ------------------------------------------------------------
# TOTAL                                      173     12    93%
# ======================================= 11 passed in 17.77s ============
# 거의 100%의 테스팅이 완료 된것을 확인 할 수 있다.


# 테스트의 커버리지 html로 출력 해보기
# pytest detector --cov=../apps/detector --cov-report=html
# (venv) PS C:\flaskbook\tests> pytest detector --cov=../apps/detector --cov-report=html
# ======================================= test session starts ==========================
# platform win32 -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0
# rootdir: C:\flaskbook\tests
# plugins: cov-7.0.0
# collected 11 items
#
# detector\test_views.py ...........                                                   [100%]
#
# ========================================= tests coverage ==================================
# __________________________ coverage: platform win32, python 3.11.2-final-0 ______________
#
# Coverage HTML written to dir htmlcov
# ================================= 11 passed in 18.15s ================================
# (venv) PS C:\flaskbook\tests>

# 탐색창에 htmlcov 디렉토리가 생성되고 index.html을 확인 할 수 있다.
