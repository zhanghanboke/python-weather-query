#!/usr/bin/env python3
"""快速测试API和城市ID"""

import requests
import json

# 配置
API_HOST = "kh3dn95ne6.re.qweatherapi.com"
JWT_TOKEN_FILE = "jwt_token.txt"

def load_jwt_token():
    with open(JWT_TOKEN_FILE, 'r') as f:
        return f.read().strip()

def test_api():
    """测试API连接和不同城市"""
    token = load_jwt_token()
    headers = {"Authorization": f"Bearer {token}"}

    # 测试的城市ID列表
    test_ids = [
        ("北京", "101010100"),
        ("上海", "101020100"),
        ("武汉", "101200101"),
        ("广州", "101280101"),
        ("深圳", "101280601"),
        ("杭州", "101210101"),
    ]

    print("=" * 60)
    print("测试不同城市ID")
    print("=" * 60)

    for city_name, city_id in test_ids:
        print(f"\n测试: {city_name} (ID: {city_id})")

        try:
            url = f"https://{API_HOST}/v7/weather/now"
            params = {"location": city_id, "lang": "zh"}

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("code") == "200":
                location = data.get("location", {})
                now = data.get("now", {})

                print(f"  ✅ 成功")
                print(f"     城市名称: {location.get('name', '未知')}")
                print(f"     城市ID: {location.get('id', '未知')}")
                print(f"     省份: {location.get('adm1', '未知')}")
                print(f"     温度: {now.get('temp', 'N/A')}°C")
                print(f"     天气: {now.get('text', 'N/A')}")
            else:
                print(f"  ❌ API错误: {data.get('message', '未知错误')}")

        except Exception as e:
            print(f"  ❌ 请求失败: {e}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
