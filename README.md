# python-weather-query
# 和风天气 (QWeather) Python 工具箱

这是一个基于 Python 的和风天气 API 调用项目，支持使用 **JWT (JSON Web Token)** 进行认证。项目集成了城市搜索、实时天气查询和数据保存等功能。

## ✨ 主要功能

*   **JWT 认证**: 支持读取 `jwt_token.txt` 进行 API 安全认证。
*   **城市搜索**: 支持模糊搜索和精确搜索，通过城市名称获取 City ID。
*   **实时天气**: 查询指定城市的实时天气数据。
*   **结果保存**: 将查询结果保存为 JSON 文件。
*   **模块化设计**: 分离了搜索、查询和工具类，便于二次开发。

## 📂 项目结构

```text
Weather/
├── weather_toolkit.py   # [推荐] 综合工具脚本，集成搜索与查询功能
├── weather_api.py       # 基础示例脚本，仅通过ID查询天气
├── city_search.py       # 城市搜索模块
├── weather_query.py     # 天气查询模块
├── jwt_token.txt        # 存放你的 JWT 令牌
├── requirements.txt     # 项目依赖
└── README.md            # 说明文档
```

## 🛠️ 环境准备

### 1. 安装 Python
确保已安装 Python 3.6 或更高版本。

### 2. 安装依赖库
运行以下命令安装所需依赖：
```bash
pip install requests cryptography PyJWT
```
> 注：`cryptography` 和 `PyJWT` 用于处理令牌相关的操作（如果需要生成或校验）。本项目核心运行依赖主要是 `requests`。

### 3. API 配置
你需要从[和风天气控制台](https://console.qweather.com/)获取以下信息：
1.  **API Host**: 例如 `kh3dn95ne6.re.qweatherapi.com` (因用户而异)。
2.  **JWT Token**: 生成一个测试用的 Token 或长期 Token。

请将你的 API Host 填入脚本中的配置区域，并将 JWT Token 内容完整粘贴到 `jwt_token.txt` 文件中。

## 🚀 使用指南

### 方式一：使用综合工具箱 (推荐)
`weather_toolkit.py` 是一个交互式的命令行工具，整合了搜索和查询功能。

```bash
python weather_toolkit.py
```

**功能菜单**:
1.  **搜索城市**: 输入名称（如“北京”、“朝阳”），获取城市 ID。
2.  **查询天气 (按ID)**: 已知 City ID 时直接查询。
3.  **搜索并查询**: 输入城市名，自动搜索并展示天气（解决了基础脚本显示“未知城市”的问题）。

### 方式二：基础查询脚本
如果你只需要简单的测试，或者只知道城市 ID，可以使用 `weather_api.py`。
请先在代码中修改 `CITY_ID` 和 `API_HOST`。

```bash
python weather_api.py
```

## 📝 开发说明

*   **API 文档**: [和风天气开发文档](https://dev.qweather.com/)
*   **城市 ID**: API 交互的核心是 Location ID，通过 `city_search.py` 模块获取。
*   **数据格式**: 所有天气数据均以 JSON 格式返回，方便后续处理。

## 🤝 贡献
欢迎提交 Issue 或 Pull Request 来改进此工具。
