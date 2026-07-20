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
    # 日经
    "znb_NKY": "JP",
    # "b_NKY": "JP",
    # TAIWAN
    "b_TWJQ": "TW",
    # UK
    "b_UKX": "UK",
    # 港股
    "rt_hkHSI": "HK",
    # "hkHSI": "HK",
    # South Kearia
    "b_KOSPI": "KR",
    # A股
    "s_sh000001": "CN",
    "s_sz399001": "CN",
    "s_sz399006": "CN",
    # Germany
    "b_DAX": "DE",
    # France
    "b_CAC": "FR",
    # Australia
    "znb_AS51": "AS",
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
        "name": "香港" + parts[1],
        "price": parts[2],
        "change": parts[7],
        "percent": parts[8],
        "time": parts[17] + " " + parts[18]
    }

def parse_cn(parts):
    return {
        "name": "缅A" + parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": "缅A实时"
    }

def parse_jp(parts):
    return {
        "name": parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": parts[6]+' '+parts[7]
    }

def parse_tw(parts):
    return {
        "name": parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": parts[6]+' '+parts[7]
    }

def parse_kr(parts):
    return {
        "name": parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": parts[6]+' '+parts[7]
    }

def parse_uk(parts):
    return {
        "name": "英国" + parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": parts[6]+' '+parts[7]
    }

def parse_de(parts):
    return {
        "name": parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": parts[6]+' '+parts[7]
    }

def parse_fr(parts):
    return {
        "name": parts[0],
        "price": parts[1],
        "change": parts[2],
        "percent": parts[3],
        "time": parts[6]+' '+parts[7]
    }

def parse_as(parts):
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
    "JP": parse_jp,
    "CN": parse_cn,
    "UK": parse_uk,
    "TW": parse_tw,
    "DE": parse_de,
    "FR": parse_fr,
    "AS": parse_as,
    "KR": parse_kr,
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
        print(parts)
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