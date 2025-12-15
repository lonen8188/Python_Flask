#                            p122                       p122
from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required  # 156 추가 (curd앱을 로그인 필수로 변경)

from apps.app import db  # p108
from apps.crud.forms import UserForm  # p120
from apps.crud.models import User  # p108

# Blueprint로 crud앱을 생성한다.

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)  # Blueprint로 crud 앱을 생성한다.
# template_folder와 static_folder를 지정하면 crud 디렉토리 내의 폴더를 이용할 수 있다.


# index 엔드포인트를 작성하고 index.html을 반환한다.
@crud.route("/")
@login_required  # p156추가 http://localhost:5000/crud/로 접속시 로그인 필수
def index():
    return render_template("crud/index.html")


@crud.route("/sql")
@login_required  # p156추가 http://localhost:5000/crud/sql로 접속시 로그인 필수
def sql():

    print("=============User테이블에 모든 정보 (세션쿼리문)==================")
    db.session.query(User).all()

    print(
        "=============User테이블에 모든 정보 (모델 객체로 처리하는 문)=================="
    )
    User.query.all()

    print("=============User테이블에 처음 1건 가져오기==================")
    db.session.query(User).first()

    print("=============User테이블에 처음 1건 가져오기 없으면 404==================")
    # db.session.query(User).first_or_404()

    print("=============User테이블에 처음 기본키 2번행 ==================")
    db.session.query(User).get(2)

    print("=============User테이블에 레코드 개수 출력 ==================")
    db.session.query(User).count()

    print("=============User테이블 페이징 처리용 ==================")
    # db.session.query(User).paginate(2, 10, False)
    # 한페이지에 10건 표시하고 2번째 페이지 표시하기 False는 error_out

    print("=============User테이블 where조건 처리용(filter_by) ==================")
    db.session.query(User).filter_by(id=2, username="admin").all()
    # filter_by는 컬럼명=값
    # id가 2이고 username이 admin인 값

    print("=============User테이블 where조건 처리용(filter) ==================")
    db.session.query(User).filter(User.id == 2, User.username == "admin").all()
    # filter는 모델명.속성==값 and조건
    # id가 2이고 username이 admin인 값

    print("=============User테이블 where조건 처리용(LIMIT) ==================")
    db.session.query(User).limit(1).all()
    # 최대 1개

    print("=============User테이블 where조건 처리용(OFFSET) ==================")
    db.session.query(User).limit(1).offset(2).all()
    # 3번째의 레코드로부터 1건 가져오기

    print("=============User테이블 where조건 처리용(ORDER BY) ==================")
    db.session.query(User).order_by("username").all()
    # username 오름차순 정렬 order_by(User.username)
    # username 내림차순 정렬 order_by(User.username.desc())
    # 여러 기준 정렬 order_by(User.age, User.username)

    print("=============User테이블 where조건 처리용(GROUP BY) ==================")
    db.session.query(User).group_by("username").all()
    # username 그룹화

    print("=======================사용자 추가 테스트=============================")
    # user = User(username="사용자명", email="kkw@mbc.com", password="1234")

    # 생성한 객체를 db에 넣는다.
    # db.session.add(user)

    # 커밋
    # db.session.commit()

    print("=======================사용자 수정 테스트=============================")
    # update 하려면 모델을 검색하여 객체를 가져오고 값을 갱신한 후 커밋
    user = db.session.query(User).filter_by(id=1).first()
    user.username = "사용자수정"
    user.email = "kkw@exmple.com"
    user.password = "4444"
    db.session.add(user)  # 객체를 db에서 가져오면 수정처리 함
    db.session.commit()

    print("=======================사용자 삭제 테스트=============================")
    # 데이터를 삭제하려면 모델을 검색하여 객체를 가져오고 삭제한 후 커밋
    user = db.session.query(User).filter_by(id=1).delete()
    db.session.commit()

    return "콘솔 로그를 확인해 주세요"


# p122 사용자 추가용
@crud.route("/users/new", methods=["GET", "POST"])
@login_required  # p156추가 http://localhost:5000/user/new로 접속시 로그인 필수
def create_user():
    # UserForm을 인스턴스화 한다.
    form = UserForm()

    # 폼의 값을 검증한다.
    if form.validate_on_submit():
        # 사용자를 작성한다.

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # 사용자를 추가하고 커밋한다.
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))  # 사용자 보기 화면으로 리다이렉트
        # 아직 users 경로가 없어 오류발생하나 테이블 보기를 해보면 들어가 있음

    return render_template("crud/create.html", form=form)


# 주의사항 : bluepring로 앱을 분할하고 템플릿을 이용하는 경우 render_template에 지정하는 html
# 값이 crud/create.html이 됨으로 주의 해야 함
# 다른 앱과 경로가 중복되지 않도록 templates 디렉토리에 앱명(crud)의 디렉터리를 만들어야 함


# 사용자 목록보기 함수 설정
@crud.route("/users")
@login_required  # p156추가 http://localhost:5000/crud/users로 접속시 로그인 필수
def users():
    # 사용자 목록보기 출력용

    users = User.query.all()
    return render_template("crud/index.html", users=users)


# 사용자 수정하기 함수 설정
@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required  # p156추가 http://localhost:5000/crud/users/<id>로 접속시 로그인 필수
def edit_user(user_id):
    form = UserForm()

    # User 모델을 이용하여 사용자를 취득한다.
    user = User.query.filter_by(id=user_id).first()

    # form으로 부터 제출된 경우 사용자를 갱신하여 사용자보기 화면으로 리다이렉트
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # GET의 경우에는 HTML을 반환한다.
    return render_template("crud/edit.html", user=user, form=form)


# 사용자 편집 화면이 표시되면 내용을 수정하고 갱신 버튼을 클릭할 수 있다.
# 여기에 비밀번호 항목에는 빈칸으로 출력되는데 보안처리를 위해서 해시화한 데이터를
# 내부적으로 보존하기 때문에 데이터를 가져올 수 없다. setter 활용


# 사용자 삭제 엔드포인트 만들기
@crud.route("/user/<user_id>/delete", methods=["POST"])
@login_required  # p156추가 http://localhost:5000/crud/users/delete로 접속시 로그인 필수
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
