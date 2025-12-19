# 같은 패키지의 config.py를 상대 import
from .config import LocalConfig

# 환경 이름 → 설정 클래스 매핑
config = {
    "local": LocalConfig,
}
