# pytest는 파이썬 서드파티 테스트 프레임 워크임
# 파이선의 표준 라이브러리인 unittest나 nose 등 테스트 프레임 워크가 있는데
# 이번에는 pytest 프레임워크를 사용해서 진행하겠다.

# pytest는 코드를 읽거나 작성하기 쉬우며 적극적으로 개발 중이다.

# pip install pytest로 설치 한다.

# 디렉토리 구성과 이름 규칙은 apps 디렉토리와 동등 위치에 tests 패키지를 작성한다.
# 여기에 샘플용 py파일을 작성하고 사용법을 배운 후 물체 감지 앱의 테스트를 작성한다.

# tests 패키지에 모듈파일(py)을 배치하는데 pytest가 테스트 코드를 검출할 수 있도록 이름 규칙이 있다.
# 테스트 모듈의 이름은 test_<something>.py 또는 <something>_test.py 와 같이 작성한다.
# 테스트 함수의 이름은 test_<something>과 같아야 한다.
# 테스트 클래스의 이름은 Test_<something>과 같아야 한다.

# pytest를 import 한다. p261 추가
import pytest


def test_func1():
    assert 1 == 1  # 가정 설정문(주장하다)
    # 콘솔에서 pytest tests 실행
    # cd tests -> pytest test_sample.py
    # pytest 3가지 방법으로 가능함

    # pytest tests
    # =============== test session starts =========================
    # platform win32 -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0
    # rootdir: C:\flaskbook
    # collected 1 item

    # tests\test_sample.py .    (뒤에 .은 테스트가 1개 실행되어 성공한것)                                                                                                                                    [100%]

    # ================ 1 passed in 0.03s ==========================

    # 콘솔에 pytest -v test_sample.py 하면 더 자세히 나옴

    # (venv) PS C:\flaskbook> cd tests
    # (venv) PS C:\flaskbook\tests> pytest -v test_sample.py
    # ============= test session starts =========================
    # platform win32 -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0 -- C:\flaskbook\venv\Scripts\python.exe
    # cachedir: .pytest_cache
    # rootdir: C:\flaskbook\tests
    # collected 1 item
    #
    # test_sample.py::test_func1 PASSED                                                                                                                             [100%]
    #
    # ============ 1 passed in 0.02s ===========================
    # (venv) PS C:\flaskbook\tests>


def test_func2():
    assert 1 == 2
    # pytest -v test_sample.py
    # ========================== test session starts ====================================
    # platform win32 -- Python 3.11.2, pytest-9.0.2, pluggy-1.6.0 -- C:\flaskbook\venv\Scripts\python.exe
    # cachedir: .pytest_cache
    # rootdir: C:\flaskbook\tests
    # collected 2 items
    #
    # test_sample.py::test_func1 PASSED                                                                                                                             [ 50%]
    # test_sample.py::test_func2 FAILED                                                                                                                             [100%]
    #
    # ============================== FAILURES =============================================
    # ______________________________ test_func2 ___________________________________________
    #
    # def test_func2():
    # >       assert 1 == 2
    # E       assert 1 == 2
    #
    # test_sample.py:51: AssertionError
    # ======================== short test summary info =====================================
    # FAILED test_sample.py::test_func2 - assert 1 == 2   (실패한 이유가 명확하게 나옴)
    # ====================== 1 failed, 1 passed in 0.16s ===================================
    # (venv) PS C:\flaskbook\tests>

    # 테스트 함수 1개만 테스트 시
    # pytest test_sample.py::test_func2
    # 공식 문서 : https://docs.pytest.org/en/stable


# pytest fixture (픽스처)
# 테스트 함수의 압뒤에 처리하는 기능
# 예를 들어 데이터베이스를 사용하는 테스트하는 경우 테스트 함수 실행전에 데이터베이스 셋팅을 실시
# 테스트 종료 후에는 클린업(데이터베이스 close : 정제)를 실시할 수 있다.


# @pytest.fixture  # 픽스처를 추가한다. p262 conftest.py로 이동한다.
# def app_data():
#    print("픽스처를 이용한 전처리")
#     return 3


# 픽스처의 함수를 인수로 지정하면 함수의 실행 결과가 달라진다.
def test_func3(app_data):
    assert app_data == 3
    # 콘솔에 pytest test_sample.py::test_func3
    # 전처리용 app_data에서 3을 리턴하여 func3에 데이터와 결합하여 처리 된다.
