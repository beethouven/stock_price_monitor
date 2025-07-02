import sys
from pathlib import Path

# 專案根目錄/src 加入 sys.path
BASE_DIR = Path(__file__).resolve().parent.parent / "src"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))