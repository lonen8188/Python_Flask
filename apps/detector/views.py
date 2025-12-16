from flask import Blueprint, render_template

from apps.app import db  # p185 추가
from apps.crud.models import User  # p185 추가
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
