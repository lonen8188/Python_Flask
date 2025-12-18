# p309 추가
from flaskbook_api.api.config.base import Config


# 로컬 환경에서만 공통의 설정
class LocalConfig(Config):
    TESTING = True
    DEBUG = True


# 만약 로컬 환경 이외에 스테이징 환경과 실제 라이브 환경이 있고
# 각각 데이터베이스에서 이용하는 데이터베이스명 등의 정보나 파라미터의
# 초깃값 등을 환경별로 나누고 싶을 때는 위와같은
# config의 분리법을 적용하면 추가/수정을 매우 간단히 할 수 있다.
