#!/usr/bin/env python3
"""
和风天气城市搜索API
支持模糊搜索、精确搜索、获取城市ID
"""

import requests
import json
from typing import List, Dict, Optional

class CitySearcher:
    """城市搜索客户端"""

    def __init__(self, api_host: str, jwt_token_file: str):
        self.api_host = api_host
        self.jwt_token_file = jwt_token_file

    def load_jwt_token(self):
        """加载JWT令牌"""
        with open(self.jwt_token_file, 'r') as f:
            return f.read().strip()

    def search_cities(self,
                     location: str,
                     adm: Optional[str] = None,
                     range_code: Optional[str] = None,
                     number: int = 10,
                     lang: str = "zh") -> List[Dict]:
        """
        搜索城市

        :param location: 城市名称（支持模糊搜索）
        :param adm: 上级行政区划（用于过滤重名城市）
        :param range_code: 搜索范围（国家代码，如"cn"）
        :param number: 返回结果数量（1-20）
        :param lang: 语言
        :return: 城市列表
        """
        token = self.load_jwt_token()
        url = f"https://{self.api_host}/geo/v2/city/lookup"

        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "location": location,
            "number": number,
            "lang": lang
        }

        # 添加可选参数
        if adm:
            params["adm"] = adm
        if range_code:
            params["range"] = range_code

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("code") != "200":
                raise ValueError(f"API错误: {data.get('message', '未知错误')}")

            return data.get("location", [])

        except Exception as e:
            raise Exception(f"城市搜索失败: {e}")

    def get_city_info(self, city_id: str) -> Optional[Dict]:
        """通过城市ID获取城市信息"""
        return self.search_cities(city_id, number=1)

    def get_city_id_by_name(self, city_name: str, adm: Optional[str] = None) -> Optional[str]:
        """通过城市名称获取城市ID（返回第一个结果）"""
        cities = self.search_cities(city_name, adm=adm, number=1)
        if cities:
            return cities[0].get("id")
        return None

    def get_city_name_by_id(self, city_id: str) -> Optional[str]:
        """通过城市ID获取城市名称"""
        city_info = self.get_city_info(city_id)
        if city_info:
            return city_info[0].get("name")
        return None


def main():
    """主函数：城市搜索演示"""
    print("=" * 70)
    print("和风天气城市搜索工具")
    print("=" * 70)

    # 配置
    API_HOST = "kh3dn95ne6.re.qweatherapi.com"
    JWT_TOKEN_FILE = "jwt_token.txt"

    searcher = CitySearcher(API_HOST, JWT_TOKEN_FILE)

    # 示例1: 精确搜索
    print("\n🔍 示例1: 精确搜索城市")
    print("-" * 70)
    try:
        cities = searcher.search_cities("北京", number=5)
        print(f"搜索'北京'，返回{len(cities)}个结果:")
        for i, city in enumerate(cities, 1):
            print(f"{i}. {city['name']} (ID: {city['id']}) - {city['adm1']}")
    except Exception as e:
        print(f"错误: {e}")

    # 示例2: 模糊搜索
    print("\n🔍 示例2: 模糊搜索城市")
    print("-" * 70)
    try:
        cities = searcher.search_cities("bei", number=5)
        print(f"搜索'bei'，返回{len(cities)}个结果:")
        for i, city in enumerate(cities, 1):
            print(f"{i}. {city['name']} (ID: {city['id']}) - {city['country']}")
    except Exception as e:
        print(f"错误: {e}")

    # 示例3: 按行政区划过滤
    print("\n🔍 示例3: 按行政区划过滤（朝阳区）")
    print("-" * 70)
    try:
        # 搜索朝阳，但只在北京市内
        cities = searcher.search_cities("朝阳", adm="北京", number=5)
        print(f"搜索'朝阳'（北京），返回{len(cities)}个结果:")
        for i, city in enumerate(cities, 1):
            print(f"{i}. {city['name']} (ID: {city['id']}) - {city['adm1']}")
    except Exception as e:
        print(f"错误: {e}")

    # 示例4: 通过城市ID获取信息
    print("\n🔍 示例4: 通过城市ID获取信息")
    print("-" * 70)
    try:
        city_id = "101010100"  # 北京
        city_info = searcher.get_city_info(city_id)
        if city_info:
            city = city_info[0]
            print(f"城市ID: {city_id}")
            print(f"城市名称: {city['name']}")
            print(f"省份: {city['adm1']}")
            print(f"国家: {city['country']}")
            print(f"经纬度: {city['lat']}, {city['lon']}")
            print(f"排名: {city['rank']}")
    except Exception as e:
        print(f"错误: {e}")

    # 交互式搜索
    print("\n" + "=" * 70)
    print("交互式搜索")
    print("=" * 70)

    while True:
        try:
            query = input("\n请输入城市名称（或输入'quit'退出）: ").strip()
            if query.lower() == 'quit':
                break

            if not query:
                continue

            # 搜索城市
            cities = searcher.search_cities(query, number=10)

            if not cities:
                print("未找到匹配的城市")
                continue

            print(f"\n找到 {len(cities)} 个匹配的城市:")
            for i, city in enumerate(cities, 1):
                print(f"{i}. {city['name']} (ID: {city['id']}) - {city['adm1']}, {city['country']}")

            # 让用户选择
            if len(cities) > 1:
                choice = input("\n请输入选择的编号（或按回车选择第一个）: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(cities):
                    selected = cities[int(choice) - 1]
                else:
                    selected = cities[0]
            else:
                selected = cities[0]

            print(f"\n✅ 选择: {selected['name']} (ID: {selected['id']})")
            print(f"   省份: {selected['adm1']}")
            print(f"   国家: {selected['country']}")
            print(f"   经纬度: {selected['lat']}, {selected['lon']}")

        except Exception as e:
            print(f"错误: {e}")

    print("\n搜索结束")


if __name__ == "__main__":
    main()
