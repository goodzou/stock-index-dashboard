import requests
import json
from pathlib import Path

codes = {
    "道琼斯": "gb_dji",
    "纳斯达克": "gb_ixic",
    "标普500": "gb_inx",
    "恒生指数": "rt_hkHSI",
    "日经225": "b_n225",
}

url = "https://hq.sinajs.cn/list=" + ",".join(codes.values())

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://finance.sina.com.cn/"
}

r = requests.get(url, headers=headers, timeout=10)

result = []

lines = r.text.strip().splitlines()

for line in lines:

    try:
        data = line.split('"')[1]
        parts = data.split(',')

        item = {
            "name": parts[0],
            "price": parts[1],
            "change": parts[4],
            "percent": parts[2],
            "time": parts[3]
        }

        result.append(item)

    except:
        pass

output = Path("docs/data.json")

output.write_text(
    json.dumps(result, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("data.json updated")