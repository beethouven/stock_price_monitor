import json

def write_json(log_list, filename):
    with open(filename, "a", encoding="utf-8") as jsonfile:
        for log in log_list:
            jsonfile.write(json.dumps(log, ensure_ascii=False) + "\n")

def read_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as jsonfile:
            return [json.loads(line) for line in jsonfile]
    except FileNotFoundError:
        print(f"檔案 {filename} 不存在，將返回空列表")
        return []

def write_sql():
    # 這個函數目前沒有實作，根據需求可以添加 SQL 寫入邏輯
    pass