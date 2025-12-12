# 사용자 신규 작성, 폼 클래스를 작성
# 사용자 신규 작성 화면의 엔트포인트를 만듬
# 신규 작성 화면의 템플릿을 만듬
# 동작을 확인

# 사용자 신규 작성, 폼 플래스 작성하기
# flask-wtf를 사용하면 폼의 값이나 데이터의 검증 설정을 클래스에서 지정할 수 있다.
# 원래는 js를 이용하여 코드를 프론트 용으로 생성

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# 사용자 신규 작성과 사용자 편짐 폼 클래스
class UserForm(FlaskForm):
    # 사용자 폼의 username 속성의 라벨과 검증을 설정한다.
    username = StringField(
        "사용자명",
        validators=[
            DataRequired(message="사용자명은 필수 입니다. "),
            Length(max=30, message="30문자 이내로 입력해 주세요!"),
        ],
    )

    # 사용자폼 email 속성의 라벨과 검증을 설정한다.
    email = StringField(
        "메일 주소",
        validators=[
            DataRequired(message="메일 주소는 필수 입니다."),
            Email(message="메일 주소 형식으로 입력해 주세요"),
        ],
    )

    # 사용자 폼 password 속성의 라벨과 검증을 설정한다.
    password = PasswordField(
        "비밀번호", validators=[DataRequired(message="비밀번호는 필수 입니다.")]
    )

    submit = SubmitField("신규 등록")
