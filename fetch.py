import requests
import json
from pathlib import Path

# =========================
# 指数代码
# =========================

CODES = {

    # 美股
    "gb_dji": "US",
    "gb_ixic": "US",
    "gb_inx": "US",

    # 港股
    "rt_hkHSI": "HK",

    # 日经
    "znb_NKY": "GLOBAL",

    # A股
    "s_sh000001": "CN",
    "s_sz399001": "CN",
    "s_sz399006": "CN",
}

# =========================
# 请求
# =========================

url = "https://hq.sinajs.cn/list=" + ",".join(CODES.keys())

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://finance.sina.com.cn/"
}

response = requests.get(
    url,
    headers=headers,
    timeout=10
)

lines = response.text.strip().splitlines()

# =========================
# 解析器
# =========================

def parse_us(parts):
    return {
        "name": parts[0],
        "price": parts[1],
        "change": parts[4],
        "percent": parts[2],
        "time": parts[3]
    }


def parse_hk(parts):
    return {
        "name": parts[1],
        "price": parts[2],
        "change": parts[7],
        "percent": parts[8],
        "time": parts[17] + " " + parts[18]
    }

def parse_a_stock(parts):
    return {
        "name": parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": "A股实时"
    }

def parse_jp(parts):
    return {
        "name": parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": parts[6]+' '+parts[7]
    }

# =========================
# 映射
# =========================

PARSERS = {
    "US": parse_us,
    "HK": parse_hk,
    "GLOBAL": parse_jp,
    "CN": parse_a_stock,
}
# =========================
# 主逻辑
# =========================

result = []
for line in lines:

    try:
        # 取代码
        code = line.split("=")[0].replace("var hq_str_", "")

        # 数据部分
        data = line.split('"')[1]

        if not data:
            continue

        parts = data.split(',')
        # print(parts)
        # 找市场类型
        market_type = CODES.get(code)

        if not market_type:
            continue

        # 找解析器
        parser = PARSERS.get(market_type)

        if not parser:
            continue

        # 解析
        item = parser(parts)
        result.append(item)

        # 输出
        # print(f"指数: {item['name']}")
        # print(f"最新: {item['price']}")
        # print(f"涨跌: {item['change']}")
        # print(f"涨幅: {item['percent']}%")
        # print(f"时间: {item['time']}")
        # print("-" * 40)


    except Exception as e:
        print("解析失败:", e)

output = Path("docs/data.json")

output.write_text(
    json.dumps(result, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("data.json updated")