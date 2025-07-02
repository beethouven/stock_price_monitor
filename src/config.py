import json
from pathlib import Path

def load_data_file(file_name, base="data"):
    path = Path(__file__).resolve().parent.parent / base / file_name
    with path.open(encoding="utf-8") as f:
        return json.load(f)