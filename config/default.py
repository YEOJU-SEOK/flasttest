import os

# 디렉터리의 깊이가 1만큼 더 늘어났으므로 os.path.dirname을 한 번 더 사용
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
