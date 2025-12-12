import apps.crud.models

# flask db init 를 이용해서 데이터베이스를 초기화 한다.
# flaskbook 아래에 migrations라는 디렉토리가 생성된다.
# 만약 디렉토리 위치를 다른곳에 하고 싶으면
# flask db init -d apps/migrations로 진행한다.
# 이후 실행하는 migrate 명령어도 -d 옵션을 넣어야 한다.

# flask db migrate 명령어
# 데이터베이스의 마이그레이션 파일을 생성하는 명령어
# 모델 정의를 바탕으로 migratings/versions 아래에
# 파이썬 파일로 데이터베이스에 적용하기 전의 정보가 생성된다.

# flask db upgrade 명령어
# 마이그레이션 정보를 실제로 데이터베이스에 반영하기 위한 명령어
# users 테이블이 생성됨


# flask db downgrade 명령어
# 마이그레이션 한 데이터베이스 적용하기 전의 상태로 되돌릴 수 있다.
