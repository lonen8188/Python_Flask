import uuid  # 파일명 랜덤 처리용
from pathlib import Path  # 파일 경로 처리용

# redirect url_for p211 추가
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required  # p211 추가(로그인 인증처리용)

from apps.app import db  # p185 추가
from apps.crud.models import User  # p185 추가
from apps.detector.forms import UploadImageForm  # p211 추가 업로드 이미지 객체
from apps.detector.models import UserImage  # p185 추가

# template_folder를 지정한다(static은 지정하지 않는다)
dt = Blueprint("detector", __name__, template_folder="templates")
# Blueprint의 static 앤드포인트의 Rule은 /<url prefix>/<static folder name>이 되는데
# dectect 앱의 경우 url_prefix를 지정하지 않았음으로 /<static folder name>이 됨


# dt 애플리케이션을 사용하여 엔드포인트를 작성한다
@dt.route("/")
def index():

    # User와 UserImage를 Join하여 이미지 일람을 취득한다 p185 추가
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )

    return render_template("detector/index.html", user_images=user_images)
    #                                                   p185 추가
    # 지금부터는 부트스트랩을 사용하여 디자인 하겠다.
    #


@dt.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
    # send_from_directory 함수에 config.py에 있는 폴더 위치와 파일명을 리턴한다.
    # images 폴더에 사진을 넣고 호출 해보자.
    # http://localhost:5000/images/파일명
    # http://localhost:5000/images/파일명


# p212 추가
@dt.route("/upload", methods=["GET", "POST"])
# 로그인 필수로 한다
@login_required
def upload_image():
    # UploadImageForm을 이용해서 밸리데이션을 한다
    form = UploadImageForm()
    if form.validate_on_submit():
        # 업로드된 이미지 파일을 취득한다
        file = form.image.data  # html <input type=filename=image>

        # 파일의 파일명과 확장자를 취득하고, 파일명을 uuid로 변환한다
        ext = Path(file.filename).suffix
        image_uuid_file_name = (
            str(uuid.uuid4()) + ext
        )  # 파일명 중복등의 이유로 변환함.(보안성)

        # 이미지를 보존한다 apps/images
        image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
        file.save(image_path)

        # DB에 보존한다
        user_image = UserImage(user_id=current_user.id, image_path=image_uuid_file_name)
        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for("detector.index"))
    return render_template("detector/upload.html", form=form)
