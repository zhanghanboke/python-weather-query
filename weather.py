#!/usr/bin/env python3
"""
和风天气JWT令牌生成器
只需填空即可使用！
"""

import time
import jwt
from pathlib import Path

# ==================== 🔴 填空区域开始 ====================
# 请将以下三个值替换为您的实际信息：

# 1. 私钥文件路径（您已经生成的ed25519-private.pem）
PRIVATE_KEY_PATH = "ed25519-private.pem"

# 2. 项目ID（从和风天气控制台获取）
PROJECT_ID = "2EKT9Y452B"  # ← 填入您的项目ID

# 3. 凭据ID（从和风天气控制台获取）
KEY_ID = "CGWFM7H6FM"  # ← 填入您的凭据ID

# 4. 令牌过期时间（分钟）
TOKEN_EXPIRY_MINUTES = 15  # ← 默认15分钟，可修改

# ==================== 🔴 填空区域结束 ====================


def generate_jwt_token():
    """生成JWT令牌"""

    # 检查私钥文件是否存在
    if not Path(PRIVATE_KEY_PATH).exists():
        raise FileNotFoundError(f"私钥文件不存在: {PRIVATE_KEY_PATH}")

    # 读取私钥
    with open(PRIVATE_KEY_PATH, 'r') as f:
        private_key = f.read()

    # 计算时间戳
    current_time = int(time.time())

    # 构建JWT Header
    headers = {
        "alg": "EdDSA",
        "kid": KEY_ID
    }

    # 构建JWT Payload
    payload = {
        "sub": PROJECT_ID,          # 项目ID
        "iat": current_time - 30,   # 签发时间（当前时间前30秒）
        "exp": current_time + (TOKEN_EXPIRY_MINUTES * 60)  # 过期时间
    }

    # 生成JWT令牌
    token = jwt.encode(
        payload,
        private_key,
        algorithm="EdDSA",
        headers=headers
    )

    return token


def main():
    """主函数"""
    print("=" * 70)
    print("和风天气JWT令牌生成器")
    print("=" * 70)

    print(f"\n配置信息:")
    print(f"  私钥文件: {PRIVATE_KEY_PATH}")
    print(f"  项目ID: {PROJECT_ID}")
    print(f"  凭据ID: {KEY_ID}")
    print(f"  过期时间: {TOKEN_EXPIRY_MINUTES}分钟")

    try:
        # 生成令牌
        print("\n⏳ 正在生成JWT令牌...")
        token = generate_jwt_token()

        # 显示令牌信息
        print("\n" + "=" * 70)
        print("✅ JWT令牌生成成功！")
        print("=" * 70)

        print(f"\n🔑 令牌内容:")
        print(f"  {token}")

        # 显示使用说明
        print(f"\n📋 使用说明:")
        print(f"  1. 在API请求中添加以下请求头:")
        print(f"     Authorization: Bearer {token}")

        print(f"\n  2. 示例curl命令:")
        print(f"     curl -H 'Authorization: Bearer {token}' \\")
        print(f"          'https://您的API主机.qweatherapi.com/v7/weather/now?location=101010100'")

        print(f"\n  3. Python代码示例:")
        print(f"     import requests")
        print(f"     headers = {{'Authorization': f'Bearer {token}'}}")
        print(f"     response = requests.get('您的APIURL', headers=headers)")

        # 保存到文件
        print(f"\n💾 是否保存令牌到文件？ (y/n): ", end="")
        save_choice = input().strip().lower()

        if save_choice == 'y':
            filename = input("请输入文件名 (默认: jwt_token.txt): ").strip() or "jwt_token.txt"
            with open(filename, 'w') as f:
                f.write(token)
            print(f"✅ 令牌已保存到: {filename}")

        print("\n" + "=" * 70)
        print("完成！")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("\n可能的原因:")
        print("1. 私钥文件路径错误")
        print("2. 项目ID或凭据ID不正确")
        print("3. 私钥文件格式错误")
        print("4. 未安装所需库: pip install cryptography PyJWT")
        print("\n请检查您的填空信息！")


if __name__ == "__main__":
    main()
