#!/usr/bin/env python3
"""
和风天气查询脚本（使用城市搜索）
先搜索城市获取准确信息，再查询天气
"""

import requests
import json
from typing import Dict, Optional

class WeatherQuery:
    """天气查询客户端"""

    def __init__(self, api_host: str, jwt_token_file: str):
        self.api_host = api_host
        self.jwt_token_file = jwt_token_file

    def load_jwt_token(self):
        """加载JWT令牌"""
        with open(self.jwt_token_file, 'r') as f:
            return f.read().strip()

    def search_city(self, city_name: str, adm: Optional[str] = None) -> Optional[Dict]:
        """
        搜索城市并返回第一个结果

        :param city_name: 城市名称
        :param adm: 上级行政区划（用于过滤重名）
        :return: 城市信息
        """
        token = self.load_jwt_token()
        url = f"https://{self.api_host}/geo/v2/city/lookup"

        headers = {"Authorization": f"Bearer {token}"}
        params = {"location": city_name, "number": 1}
        if adm:
            params["adm"] = adm

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get("code") != "200":
                return None

            locations = data.get("location", [])
            return locations[0] if locations else None

        except Exception as e:
            print(f"城市搜索失败: {e}")
            return None

    def get_weather_now(self, city_id: str) -> Optional[Dict]:
        """
        获取实时天气

        :param city_id: 城市ID
        :return: 天气数据
        """
        token = self.load_jwt_token()
        url = f"https://{self.api_host}/v7/weather/now"

        headers = {"Authorization": f"Bearer {token}"}
        params = {"location": city_id, "lang": "zh"}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get("code") != "200":
                print(f"API错误: {data.get('message', '未知错误')}")
                return None

            return data

        except Exception as e:
            print(f"天气查询失败: {e}")
            return None

    def query_weather_by_city(self, city_name: str, adm: Optional[str] = None) -> Optional[Dict]:
        """
        通过城市名称查询天气

        :param city_name: 城市名称
        :param adm: 上级行政区划（用于过滤重名）
        :return: 天气数据
        """
        # 先搜索城市
        print(f"🔍 搜索城市: {city_name}...")
        city_info = self.search_city(city_name, adm)

        if not city_info:
            print(f"❌ 未找到城市: {city_name}")
            return None

        print(f"✅ 找到城市: {city_info['name']} (ID: {city_info['id']})")
        print(f"   位置: {city_info['adm1']}, {city_info['country']}")

        # 再查询天气
        print(f"🔄 查询天气...")
        weather_data = self.get_weather_now(city_info["id"])

        if weather_data:
            # 将城市信息添加到天气数据中
            weather_data["city_info"] = city_info

        return weather_data

    def format_weather_result(self, weather_data: Dict) -> str:
        """格式化天气结果"""
        if not weather_data or "now" not in weather_data:
            return "未获取到天气数据"

        now = weather_data["now"]
        city_info = weather_data.get("city_info", {})

        # 提取城市名称
        city_name = city_info.get("name", "未知城市")

        # 构建结果
        result = f"\n{'='*60}\n"
        result += f"🌤️  {city_name} 实时天气\n"
        result += f"{'='*60}\n"

        result += f"城市信息:\n"
        result += f"  名称: {city_info.get('name', '未知')}\n"
        result += f"  ID: {city_info.get('id', '未知')}\n"
        result += f"  位置: {city_info.get('adm1', '未知')}, {city_info.get('country', '未知')}\n"
        result += f"  经纬度: {city_info.get('lat', '未知')}, {city_info.get('lon', '未知')}\n"

        result += f"\n天气数据:\n"
        result += f"  更新时间: {now.get('obsTime', '未知时间').replace('T', ' ')}\n"
        result += f"  温度: {now.get('temp', 'N/A')}°C\n"
        result += f"  天气状况: {now.get('text', 'N/A')}\n"
        result += f"  体感温度: {now.get('feelsLike', 'N/A')}°C\n"
        result += f"  风向: {now.get('windDir', 'N/A')}\n"
        result += f"  风力: {now.get('windScale', 'N/A')}级\n"
        result += f"  湿度: {now.get('humidity', 'N/A')}%\n"
        result += f"  气压: {now.get('pressure', 'N/A')} hPa\n"

        result += f"{'='*60}\n"
        return result


def main():
    """主函数：天气查询演示"""
    print("=" * 70)
    print("和风天气查询工具（先搜索城市，再查天气）")
    print("=" * 70)

    # 配置
    API_HOST = "kh3dn95ne6.re.qweatherapi.com"
    JWT_TOKEN_FILE = "jwt_token.txt"

    querier = WeatherQuery(API_HOST, JWT_TOKEN_FILE)

    # 示例1: 查询北京天气
    print("\n🔍 示例1: 查询北京天气")
    print("-" * 70)
    weather = querier.query_weather_by_city("北京")
    if weather:
        print(querier.format_weather_result(weather))

    # 示例2: 查询上海天气
    print("\n🔍 示例2: 查询上海天气")
    print("-" * 70)
    weather = querier.query_weather_by_city("上海")
    if weather:
        print(querier.format_weather_result(weather))

    # 示例3: 查询武汉天气（你之前查询的城市）
    print("\n🔍 示例3: 查询武汉天气")
    print("-" * 70)
    weather = querier.query_weather_by_city("武汉")
    if weather:
        print(querier.format_weather_result(weather))

    # 示例4: 查询朝阳区（需要指定行政区划）
    print("\n🔍 示例4: 查询北京市朝阳区天气")
    print("-" * 70)
    weather = querier.query_weather_by_city("朝阳", adm="北京")
    if weather:
        print(querier.format_weather_result(weather))

    # 交互式查询
    print("\n" + "=" * 70)
    print("交互式天气查询")
    print("=" * 70)

    while True:
        try:
            city = input("\n请输入城市名称（或输入'quit'退出）: ").strip()
            if city.lower() == 'quit':
                break

            if not city:
                continue

            # 查询天气
            weather = querier.query_weather_by_city(city)

            if weather:
                print(querier.format_weather_result(weather))
            else:
                print(f"❌ 无法获取 {city} 的天气")

        except Exception as e:
            print(f"错误: {e}")

    print("\n查询结束")


if __name__ == "__main__":
    main()
