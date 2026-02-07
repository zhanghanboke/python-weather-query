#!/usr/bin/env python3
"""
和风天气API调用脚本
使用生成的JWT令牌查询天气
"""

import requests
import json

# ==================== 🔴 填空区域 ====================
# 请将以下值替换为您的实际信息：

# 1. 您的API Host（从控制台获取）
API_HOST = "kh3dn95ne6.re.qweatherapi.com"  # ← 填入您的API Host

# 2. 读取JWT令牌
JWT_TOKEN_FILE = "jwt_token.txt"  # 令牌文件路径

# 3. 查询的城市ID（北京为101010100，可替换为其他城市）
CITY_ID = "101010100"  # ← 可修改为其他城市ID
# ====================================================


def load_jwt_token():
    """从文件加载JWT令牌"""
    try:
        with open(JWT_TOKEN_FILE, 'r') as f:
            token = f.read().strip()
        return token
    except FileNotFoundError:
        raise FileNotFoundError(f"JWT令牌文件不存在: {JWT_TOKEN_FILE}")


def get_weather_now(city_id):
    """
    获取实时天气

    :param city_id: 城市ID
    :return: 天气数据
    """
    # 加载JWT令牌
    token = load_jwt_token()

    # 构建API URL
    api_url = f"https://{API_HOST}/v7/weather/now"

    # 设置请求头
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # 设置查询参数
    params = {
        "location": city_id,
        "lang": "zh"  # 返回中文数据
    }

    try:
        # 发送请求
        response = requests.get(
            api_url,
            headers=headers,
            params=params,
            timeout=10
        )

        # 检查响应状态
        response.raise_for_status()

        # 解析JSON响应
        data = response.json()

        # 检查API返回的code
        if data.get("code") != "200":
            raise ValueError(f"API错误: {data.get('message', '未知错误')}")

        return data

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"网络请求失败: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON解析失败: {e}")


def format_weather_data(weather_data):
    """格式化天气数据为可读格式"""
    if not weather_data or "now" not in weather_data:
        return "未获取到天气数据"

    now = weather_data["now"]
    location = weather_data.get("location", {})

    # 提取关键信息
    info = {
        "城市": location.get("name", "北京"),
        "更新时间": now.get("obsTime", "未知时间").replace("T", " "),
        "温度": f"{now.get('temp', 'N/A')}°C",
        "天气状况": now.get("text", "N/A"),
        "体感温度": f"{now.get('feelsLike', 'N/A')}°C",
        "风向": now.get("windDir", "N/A"),
        "风力": f"{now.get('windScale', 'N/A')}级",
        "湿度": f"{now.get('humidity', 'N/A')}%",
        "气压": f"{now.get('pressure', 'N/A')} hPa"
    }

    # 构建格式化字符串
    result = f"\n{'='*50}\n"
    result += f"🌤️  {info['城市']} 实时天气\n"
    result += f"{'='*50}\n"

    for key, value in info.items():
        result += f"  {key}: {value}\n"

    result += f"{'='*50}\n"
    return result


def main():
    """主函数"""
    print("=" * 60)
    print("和风天气API调用工具")
    print("=" * 60)

    print(f"\n配置信息:")
    print(f"  API Host: {API_HOST}")
    print(f"  令牌文件: {JWT_TOKEN_FILE}")
    print(f"  查询城市ID: {CITY_ID}")

    try:
        # 1. 获取实时天气
        print(f"\n🔄 正在查询城市 {CITY_ID} 的天气...")
        weather_data = get_weather_now(CITY_ID)

        # 2. 格式化并显示数据
        print(format_weather_data(weather_data))

        # 3. 询问是否查询其他城市
        print("\n是否查询其他城市？ (y/n): ", end="")
        if input().strip().lower() == 'y':
            city_id = input("请输入城市ID (如: 101020100-上海): ").strip()
            if city_id:
                try:
                    weather_data = get_weather_now(city_id)
                    print(format_weather_data(weather_data))
                except Exception as e:
                    print(f"❌ 查询失败: {e}")

        # 4. 保存结果到文件
        print("\n是否保存结果到文件？ (y/n): ", end="")
        if input().strip().lower() == 'y':
            filename = input("请输入文件名 (默认: weather_result.json): ").strip() or "weather_result.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(weather_data, f, ensure_ascii=False, indent=2)
            print(f"✅ 结果已保存到: {filename}")

        print("\n" + "=" * 60)
        print("操作完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("\n可能的原因:")
        print("1. API Host不正确")
        print("2. JWT令牌文件不存在或已过期")
        print("3. 网络连接问题")
        print("4. 城市ID不正确")
        print("5. API调用次数已用完（检查控制台）")

        print("\n排查建议:")
        print("1. 检查API Host是否正确")
        print("2. 确认JWT令牌是否已过期（15分钟有效期）")
        print("3. 重新生成JWT令牌并重试")
        print("4. 检查网络连接")


if __name__ == "__main__":
    main()
