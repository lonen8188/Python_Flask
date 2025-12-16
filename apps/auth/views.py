# from flask import Blueprint, render_template P153변경
from flask import Blueprint, flash, redirect, render_template, request, url_for

# from flask_login import login_user   p162변경
# from flask_login import login_user, logout_user p162 변경
from flask_login import login_user, logout_user

from apps.app import db

# from apps.auth.forms import SignUpForm  # p159 추가 LoginForm
from apps.auth.forms import LoginForm, SignUpForm
from apps.crud.models import User  # P153 여기까지

# Blueprint 를 사용해서 auth를 생성한다.
auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


# index 엔드 포인트를 작성한다.
@auth.route("/")
def index():
    return render_template("auth/index.html")
    # 프론트 페이지를 작성한다.
    # apps/auth/templates/auth/base.html


# P154 추가 회원가입 엔드포인트 만들기
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # SignUpForm을 인스턴스화한다
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # 메일 주소 중복 체크를 한다
        if user.is_duplicate_email():
            flash("지정한 이메일 주소는 이미 등록되어 있습니다.")
            return redirect(url_for("auth.signup"))

        # 사용자 정보를 등록한다
        db.session.add(user)
        db.session.commit()

        # 사용자 정보를 세션에 저장한다
        login_user(user)

        # GET 파라미터에 next 키가 존재하고, 값이 없는 경우는 사용자의 일람 페이지로 리다이렉트한다
        # 인증되지 않았을 때 인증 필수 화면에 접속하면 회원가입(사용자 신규등록) 화면으로 리다이렉트되지만,
        # 그 경우 GET 파라미터의 next 키에 접근하려고 한 페이지의 엔드포인트가 붙는다.
        # next 키에 값이 있는 경우는 회원가입에 성공하면 next 키의 페이지로 리다이렉트하고, 값이 없는 경우
        # 사용자 일람 페이지로 리다이렉트 한다.
        # 사용자 정보를 세션에 저장하고 있으므로 리다이렉트 후는 로그인 상태가 됨
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            # next_ = url_for("crud.users") p197변경
            next_ = url_for("detector.index")
            # 회원가입시 리다이렉트 경로 변경 (객체감지용 인덱스 페이지)
        return redirect(next_)

    return render_template("auth/signup.html", form=form)


# 회원가입 기능의 템플릿 만들기 apps/auth/templates/auth/signup.html 생성


# 로그인 기능을 위해서 엔드포인트 만들기
# p159 추가
@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # 메일 주소로부터 사용자를 취득한다
        user = User.query.filter_by(email=form.email.data).first()

        # 사용자가 존재하고 비밀번호가 일치하는 경우는 로그인을 허가한다
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            # p201 교체
            # return redirect(url_for("crud.users"))
            return redirect(url_for("detector.index"))

        # 로그인 실패 메시지를 설정한다
        flash("메일 주소 또는 비밀번호가 일치하지 않습니다")
    return render_template("auth/login.html", form=form)
    # 로그인 프론트 페이지 생성 apps/auth/templates/auth/login.html


# p162 로그아웃 추가 엔드포인트 생성
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
