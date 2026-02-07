#!/usr/bin/env python3
"""
和风天气完整工具
集成城市搜索、天气查询、数据保存
"""

import requests
import json
import time
from typing import Dict, List, Optional

class WeatherToolkit:
    """天气工具箱"""

    def __init__(self, api_host: str, jwt_token_file: str):
        self.api_host = api_host
        self.jwt_token_file = jwt_token_file
        self.cache = {}  # 简单的缓存

    def load_jwt_token(self):
        """加载JWT令牌"""
        with open(self.jwt_token_file, 'r') as f:
            return f.read().strip()

    def search_city(self, city_name: str, adm: Optional[str] = None,
                   range_code: Optional[str] = None, number: int = 10) -> List[Dict]:
        """
        搜索城市

        :param city_name: 城市名称（支持模糊搜索）
        :param adm: 上级行政区划（用于过滤重名）
        :param range_code: 搜索范围（国家代码）
        :param number: 返回结果数量
        :return: 城市列表
        """
        cache_key = f"search_{city_name}_{adm}_{range_code}_{number}"
        if cache_key in self.cache:
            # 检查缓存是否过期（1小时）
            if time.time() - self.cache[cache_key]["timestamp"] < 3600:
                return self.cache[cache_key]["data"]

        token = self.load_jwt_token()
        url = f"https://{self.api_host}/geo/v2/city/lookup"

        headers = {"Authorization": f"Bearer {token}"}
        params = {"location": city_name, "number": number}
        if adm:
            params["adm"] = adm
        if range_code:
            params["range"] = range_code

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get("code") != "200":
                return []

            locations = data.get("location", [])

            # 缓存结果
            self.cache[cache_key] = {
                "timestamp": time.time(),
                "data": locations
            }

            return locations

        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def get_weather_now(self, city_id: str) -> Optional[Dict]:
        """获取实时天气"""
        cache_key = f"weather_{city_id}"
        if cache_key in self.cache:
            if time.time() - self.cache[cache_key]["timestamp"] < 300:  # 5分钟缓存
                return self.cache[cache_key]["data"]

        token = self.load_jwt_token()
        url = f"https://{self.api_host}/v7/weather/now"

        headers = {"Authorization": f"Bearer {token}"}
        params = {"location": city_id, "lang": "zh"}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data.get("code") != "200":
                return None

            # 缓存结果
            self.cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }

            return data

        except Exception as e:
            print(f"天气查询失败: {e}")
            return None

    def save_weather_data(self, weather_data: Dict, filename: str):
        """保存天气数据到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=2)
            print(f"✅ 数据已保存到: {filename}")
        except Exception as e:
            print(f"保存失败: {e}")

    def format_city_list(self, cities: List[Dict]) -> str:
        """格式化城市列表"""
        if not cities:
            return "未找到匹配的城市"

        result = f"找到 {len(cities)} 个城市:\n"
        for i, city in enumerate(cities, 1):
            result += f"{i}. {city['name']} (ID: {city['id']})\n"
            result += f"   位置: {city.get('adm1', '未知')}, {city.get('country', '未知')}\n"
            result += f"   经纬度: {city.get('lat', '未知')}, {city.get('lon', '未知')}\n"
            result += f"   排名: {city.get('rank', '未知')}\n\n"

        return result

    def format_weather(self, weather_data: Dict, city_info: Dict) -> str:
        """格式化天气信息"""
        if not weather_data or "now" not in weather_data:
            return "未获取到天气数据"

        now = weather_data["now"]

        result = f"\n{'='*60}\n"
        result += f"🌤️  {city_info.get('name', '未知城市')} 实时天气\n"
        result += f"{'='*60}\n"

        result += f"📍 城市信息:\n"
        result += f"  名称: {city_info.get('name', '未知')}\n"
        result += f"  ID: {city_info.get('id', '未知')}\n"
        result += f"  位置: {city_info.get('adm1', '未知')}, {city_info.get('country', '未知')}\n"
        result += f"  经纬度: {city_info.get('lat', '未知')}, {city_info.get('lon', '未知')}\n"

        result += f"\n🌡️  天气数据:\n"
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
    """主函数：完整工具演示"""
    print("=" * 70)
    print("和风天气完整工具")
    print("=" * 70)

    # 配置
    API_HOST = "kh3dn95ne6.re.qweatherapi.com"
    JWT_TOKEN_FILE = "jwt_token.txt"

    toolkit = WeatherToolkit(API_HOST, JWT_TOKEN_FILE)

    # 示例1: 城市搜索
    print("\n🔍 示例1: 城市搜索")
    print("-" * 70)
    cities = toolkit.search_city("北京", number=5)
    print(toolkit.format_city_list(cities))

    # 示例2: 查询天气
    print("\n🔍 示例2: 查询天气")
    print("-" * 70)
    # 先搜索城市获取ID
    cities = toolkit.search_city("北京", number=1)
    if cities:
        city_info = cities[0]
        print(f"搜索到城市: {city_info['name']} (ID: {city_info['id']})")

        # 查询天气
        weather = toolkit.get_weather_now(city_info["id"])
        if weather:
            print(toolkit.format_weather(weather, city_info))

    # 示例3: 模糊搜索 + 天气
    print("\n🔍 示例3: 模糊搜索 + 天气查询")
    print("-" * 70)
    query = "bei"
    cities = toolkit.search_city(query, number=3)
    print(f"搜索 '{query}'，找到 {len(cities)} 个城市:")
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city['name']} (ID: {city['id']}) - {city['country']}")

    # 交互式工具
    print("\n" + "=" * 70)
    print("交互式工具")
    print("=" * 70)

    while True:
        print("\n请选择操作:")
        print("1. 搜索城市")
        print("2. 查询天气")
        print("3. 搜索并查询天气")
        print("4. 退出")

        choice = input("\n请输入选择 (1-4): ").strip()

        if choice == "1":
            # 搜索城市
            city = input("请输入城市名称: ").strip()
            adm = input("请输入行政区划（可选，按回车跳过）: ").strip()
            adm = adm if adm else None

            cities = toolkit.search_city(city, adm=adm, number=10)
            print(toolkit.format_city_list(cities))

            if cities:
                save = input("\n是否保存结果到文件？(y/n): ").strip().lower()
                if save == "y":
                    filename = input("请输入文件名 (默认: city_search.json): ").strip() or "city_search.json"
                    toolkit.save_weather_data({"cities": cities}, filename)

        elif choice == "2":
            # 查询天气
            city_id = input("请输入城市ID: ").strip()
            weather = toolkit.get_weather_now(city_id)

            if weather:
                # 获取城市信息
                cities = toolkit.search_city(city_id, number=1)
                city_info = cities[0] if cities else {"name": "未知城市", "id": city_id}

                print(toolkit.format_weather(weather, city_info))

                save = input("\n是否保存结果到文件？(y/n): ").strip().lower()
                if save == "y":
                    filename = input("请输入文件名 (默认: weather.json): ").strip() or "weather.json"
                    toolkit.save_weather_data(weather, filename)

        elif choice == "3":
            # 搜索并查询天气
            city = input("请输入城市名称: ").strip()
            adm = input("请输入行政区划（可选，按回车跳过）: ").strip()
            adm = adm if adm else None

            cities = toolkit.search_city(city, adm=adm, number=1)

            if not cities:
                print("未找到匹配的城市")
                continue

            # 选择城市
            if len(cities) > 1:
                print(toolkit.format_city_list(cities))
                choice = input("请选择编号（按回车选择第一个）: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(cities):
                    city_info = cities[int(choice) - 1]
                else:
                    city_info = cities[0]
            else:
                city_info = cities[0]

            print(f"\n选择: {city_info['name']} (ID: {city_info['id']})")

            # 查询天气
            weather = toolkit.get_weather_now(city_info["id"])
            if weather:
                print(toolkit.format_weather(weather, city_info))

                save = input("\n是否保存结果到文件？(y/n): ").strip().lower()
                if save == "y":
                    filename = input("请输入文件名 (默认: weather.json): ").strip() or "weather.json"
                    # 保存完整数据
                    full_data = {
                        "city_info": city_info,
                        "weather": weather
                    }
                    toolkit.save_weather_data(full_data, filename)

        elif choice == "4":
            print("退出工具")
            break

        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()
