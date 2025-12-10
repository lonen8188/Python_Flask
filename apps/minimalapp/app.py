# 플라스크 클래스를 가져온다.

# p68 이메일 인증용 객체 삽입
import logging

# p76추가 이메일 처리용
import os

# .env 활성화 코드
from dotenv import load_dotenv

load_dotenv()
from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension  # p73추가
from flask_mail import Mail, Message  # p76추가

# 플라스크 클래스를 객체로 만든다.
app = Flask(__name__)

# SECRET_KET를 추가한다. P68
app.config["SECRET_KEY"] = "12345678901234567890"
# pip install email-validator 를 설치한다.

# p72 로그레벨 설정 추가
app.logger.setLevel(logging.DEBUG)

# 플라스크의 로그처리용 모듈이 flask-debugtoolbar라고 있다.
# http 요청이나 flask router 결과, 데이터베이스 발행 sql등을 확인 할 수 있다.
# pip install flask-debugtoolbar
# 상단에 from flask_debugtoolbar import DebugToolbarExtension 추가

# 리다이렉트를 중단하지 않도록 한다.
# 리다이렉트하면 요청한 값을 flask-debugtoolbar에서 확인 할 수 없다. 기본값(true)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# DebugToolbarExtension에 애플리케이션을 설정한다. (import한 내용 연결)
toolbar = DebugToolbarExtension(app)

# p74 이메일 보내기 추가
# pip install flask-mail
# flask-mail의 설정값 정리
# 설정                기본값             설명
# MAIL_SERVER           localhost        이메일 서버의 호스트명
# MAIL_PORT             25               이메일 서버의 포트(SMTP)
# MAIL_USE_TLS          False            tls 유효 설정
# MAIL_USE_SSL          False            ssl 유효 설정
# MAIL_DEBUG            app.debug        디버그 모드
# MAIL_USERNAME         None             송신자 이메일 주소
# MAIL_PASSWORD         None             송신자 이메일 주소의 비번
# MAIL_DEFAULT_SENDER   None             이메일 송신자명과 이메일 주소

# gmail계정으로 이메일 처리 해보자.
# https://velog.io/@meanseo/flask-flask%EC%97%90%EC%84%9C-gmail%EB%A1%9C-%EC%9D%B8%EC%A6%9D-%EB%A9%94%EC%9D%BC-%EB%B3%B4%EB%82%B4%EA%B8%B0
# 상단에 import os 를 추가한다.

# Mail 클래스의 config를 추가한다. p77
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "True") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장 등록을 한다.
mail = Mail(app)  # .env에 환경설정 값을 추가한다.


# http://localhost:5000/ 경로를 생성한다.
@app.route("/")
def index():
    return "Hello, FlaskBook!!!"


# http://localhost:5000/hello
@app.route("/hello", endpoint="hello-endpoint")
def hello():
    return "Hello, MBCAI!!!"


# http://localhost:5000/name/kkw
@app.route("/name/<name>", endpoint="show_name")
def show_name(name):  # 인자값으로 name 필수
    # return f"Hello, {name}!!"
    return render_template("index.html", name=name)


# 애플리케이션 컨텍스트 / 요청 컨텍스트
# 애플리케이션 컨텍스트 : 요청을 통해 앱 레벨의 데이터를 이용할 수 있도록 하는 것
# 애플리케이션 레벨 데이터는 current_app과 g가 있다.
# current_app : 액티브 앱(실행 중의 앱)의 인스턴스
# g : 요청을 통해 이용할 수 있는 전역 임시(일시) 영역, 요청마다 리셋됨

# 지금까지 app = Flask(__name__)로 취득한 app에 접근하면 앱의 인스턴스에 접근 할 수 있었지만
# 앱 규모가 커지면 상호 참조해 순환이 생기는 순환참조가 발생하기 쉬워지고
# 플라스크 측에서 오류가 발생함
# 플라스크는 이 문제를 해결하기 위해 플라스크 앱의 인스턴스인 app을 직접 참조하는 것이 아니라,
# current_app에 접근 한다.
# 애플리케이션 컨텍스트인 current_app은 플라스크에 요청 처리를 하면 스택에 push되어서
# current_app이라는 속성에 접근할 수 있게 됨
# 스택(일시적으로 테이터를 저장하는 데이터 구조)
# 푸쉬(push : 데이터를 쌓는 것)
# 팝(pop : 데이터를 꺼내는 것)

# print(current_app) 이라고 쓰고 저장하면 플라스크 런에서 에러 발생 - 주석처리
#   File "C:\flaskbook\venv\Lib\site-packages\werkzeug\local.py", line 519, in _get_current_object
#    raise RuntimeError(unbound_message) from None
# RuntimeError: Working outside of application context.

# 애플리케이션 컨텍스트를 취득하여 스택에 push한다.
ctx = app.app_context()  # 인스턴스 생성
ctx.push()

# current_app에 접근 해보자.
print(current_app.name)  # 콘솔에 apps.minimalapp.app이라고 나옴

# 전역 임시 영역에 값을 설정한다.
g.connection = "connection"
print(g.connection)  # 콘솔에 connection이 출력된다.

# current_app은 애플리케이션 컨텍스트로부터 push 되면 스택에 쌓여서 어디에서나 접근
# g는 요청을 통해 이용할 수 있는 전역 임시영역인데
# g도 마찬가지로 애플리케이션 컨텍스트가 스택에 쌓이면 이용할 수 있다.
# g의 대표적인 이용은 데이터베이스 연결에 해당하며 g에 설정한 값은 동일한 요청이 있는 동안
# 어디에서나 접근할 수 있게 된다.

# 요청 컨텍스트
# 요청이 있는 동안 요청 레벨의 데이터를 이용할수 있도록 하는 것
# 요청 레벨의 데이터에는 request와 session이 있다.
# 요청 컨텍스트를 수동으록 취득하여 푸시하려면 url_for함수를 사용해 url을 생성한다.
# with app.test_request_context("/user?updated=true"):
# session은 서버자체가 가지고 있는 접속영역으로 로그인 유지 등 을 사용한다.

# PRG 패턴
# POST -> REDIRECT -> GET패턴의 약어
# 문의 폼 화면(GET) -> 이메일 송신(POST) -> 문의완료 화면으로 보냄(REDIRECT) -> 문의완료 화면 표시(GET)
# PRG 패턴을 사용하지 않으면 POST가 이중으로 전송될 가능성이 있다.(새로고침 문제)

# 문의 폼 요약
# ENDPOINT          METHODS       RULE
# contact           get           /contact
# contact_complete  get,post      /contact/complete

# 문의 폼 만들기 상단에 redirect 추가
# request의 속성, 메서드 설명
# method : 요청 메서드
# form : 요청 폼
# args : 쿼리 파라미터
# cookies : 요청 쿠키(Cookie)
# files : 요청 파일
# environ : 환경 변수
# headers : 요청 헤더
# referrer : 요청 리퍼러(링크 참조 페이지)
# query_string : 요청쿼리 문자열
# Scheme : 요청 프로토콜(http/https)
# url : 요청 url


@app.route("/contact")  # http://localhost:5000/contact
def contact():
    # 응답 객체를 가져온다. p84 추가
    response = make_response(render_template("contact.html"))

    # 쿠키를 설정한다.
    response.set_cookie("flaskbook key", "flaskbook value")

    # 세션을 설정한다.
    session["username"] = "kkw"

    # 응답 객체를 반환한다.
    return response


# Flash 메시지 p67추가
# Flash 메시지는 동작 실행 후 간단한 메시지를 표시하는 기능으로 완료시나 오류발생시 일시적으로 메시지를 표시함
# 유효성 검증용 코드 : 문의 폼 화면에 유효성 검증코드를 추가해본다.
# Flash 메시지는 flash 함수를 사용하여 설정하고 템플릿에서 get_flashed_messages 함수를 사용하여 표시
# Flash 메시지를 이용하려면 세션이 필요함 config의 SECRET_KEY를 설정 해야 함


# http://localhost:5000/contact/complete
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form 속성을 사용해서 폼의 값을 가져온다. p67
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 입력 폼 검증 코드
        is_valid = True

        if not username:
            flash("사용자 명은 필수 입니다.")
            is_valid = False

        if not email:
            flash("메일 주소는 필수 입니다.")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력 해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수 입니다.")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # .env에 내용 확인용 코드
        print("MAIL_USERNAME:", app.config["MAIL_USERNAME"])
        print("MAIL_PASSWORD:", app.config["MAIL_PASSWORD"])
        print("MAIL_SERVER:", app.config["MAIL_SERVER"])
        print("MAIL_PORT:", app.config["MAIL_PORT"])
        print("MAIL_USE_TLS:", app.config["MAIL_USE_TLS"])

        # 이메일 전송코드 추가 p78
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        flash("문의해 주셔서 감사합니다.")
        return redirect(url_for("contact_complete"))
        # 메서드가 POST로 요청이 들어오면 앤드포인트로 리다이렉트 한다.

    return render_template("contact_complete.html")
    # GET인 경우에는 문의 완료 화면을 반환


# 로깅 기능
# 개발 시나 운용 시에 예기치 않은 오류가 발생하는 경우 콘솔이나 파일로 확인하는 기법
# 로거에는 로그 레벨이 존재하며 지정한 로그보다 높은 로그들만 출력함
# 로그 레벨
# CRITICAL : 치명적 오류 (프로그램의 이상 종료를 수반하는 것과 같은 오류)
# ERROR : 오류 (예기치 않은 실행시 오류)
# WARNING : 경고 (오류에 가까운 현상 : 준_정상계(Abnormal))
# INFO : 정보 (정상 동작의 확인에 필요한 정보)
# DEBUG : 개발시 필요한 정보
# 플라스크는 파이썬 표준 logging 모듈을 이용함
# 상단에 import loggin 추가
app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")


def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


# 쿠키 p81
# 쿠키는 클라이언트의 브라우저와 웹 서버 사이에서 상태를 관리하기 위해서 브라우져에 저장된 정보
# 로그인 기억 / 이번주 보지 않기 광고창
# 플라스크에서 쿠키로 부터 값을 취득하는 데는 요청 객체(request)를 사용
# 값의 설정에는 make_response로 얻은 응답객체(response)를 사용
# 상단에 from flask import request 작성

# username = request.cookies.get("username")  # 쿠키에 있는 username을 가져온다.

# 쿠키로 값을 설정하기
# from flask import make_response, render_template

# response = make_response(render_template("contact.html"))

# key와 value를 설정한다. max_age=30초
# response.set_cookie("username", "kkw", max_age=30)

# 쿠키로부터 값을 삭제하기
# response = make_response(render_template("contact.html"))
# key값으로 삭제한다.
# response.delete_cookie("username")
# response.set_cookie("username", "", max_age=0)로 사용가능


# 세션(사용자의 로그인 정보 등을 서버에 유지하고, 일련의 처리를 계속적으로 실시)
# http는 스테이트리스이므로 상태를 유지할 수 없지만, 쿠키를 사용한 세션관리 구조를 사용함으로 연속적인 처리가 가능
# 스테이트리스 : 서버가 클라이언트의 정보를 유지하지 않아 웹 서버측에서 상태를 관리할 수 없는 것!

# 로그인 상태 유지 등....
# 1. 사용자가 로그인 조작을 함
# 2. 서버는 세션 id를 발생하고 사용자의 정보를 연결하여 정보를 유지
# 3. 세션ID를 브라우져 쿠키에 저장
# 4. 이후 요청시 보내지는 쿠키로부터 세션ID를 취득하고 연결된 사용자를 취득
# 5. 취득한 사용자에게 필요한 처리를 하거나 정보를 반환

# 세션에 값 설정하기
# from flask import session
# session["username"] = "kkw" 세션키 username / 값 kkw
# username = session["username"] 세션에 username 키값을 가져와 username 변수에 넣음
# session.pop("username", None) 세션값 삭제하기

# return render_template("contact_complete.html") 플라스크에서는 통상 이렇게 필요한 값을 응답으로 반환함
# 쿠키에 값을 설정하는 등 등답의 내용을 갱신해야 하는 경우에는 make_response함수를 사용

# response의 속성 및 메서드
# status_code   응답 상태 코드 (200, 300, 400, 500)
# headers       응답 헤더
# set_cookie    쿠키를 설정한다.
# delete_cookie 쿠키를 삭제한다.


# url_for 사용해보기
with app.test_request_context("/user?updated=true"):
    #                          p59 추가
    # http://localhost:5000/
    print(url_for("index"))
    # http://localhost:5000/hello
    print(url_for("hello-endpoint", name="world"))
    # http://localhost:5000/mbc/kkw?page=1
    print(url_for("show_name", name="kkw", page="1"))
    # 콘솔에 true가 출력 된다.
    print(request.args.get("updated"))
