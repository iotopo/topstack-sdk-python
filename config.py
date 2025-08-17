"""
TopStack Python SDK 配置文件

请根据您的实际环境修改以下配置参数
"""

# TopStack 服务配置
TOPSTACK_CONFIG = {
    # TopStack 服务地址
    "base_url": "http://localhost:8000",
    
    # 应用 ID - 请替换为您的实际应用 ID
    "app_id": "your-app-id",
    
    # 应用密钥 - 请替换为您的实际应用密钥
    "app_secret": "your-app-secret",
    
    # 请求超时时间（秒）
    "timeout": 30,
    
    # 是否验证 SSL 证书（开发环境建议设为 False）
    "verify_ssl": False
}

# 测试设备配置
TEST_DEVICES = {
    # 测试设备 ID
    "device_id": "dev1",
    
    # 测试测点 ID
    "point_id": "v1",
    
    # 控制测点 ID
    "control_point_id": "V4"
}

# 数据可视化配置
DATAV_CONFIG = {
    # 页面 ID
    "page_id": "ct9avosgj6lmas2l2hl0",
    
    # 访问令牌
    "token": "8061337fe3e34be1bf0ee1a4e15d3a63",
    
    # 用户名（可选）
    "username": "",
    
    # 密码（可选）
    "password": ""
}

# 历史数据查询配置
HISTORY_CONFIG = {
    # 查询时间范围（分钟）
    "time_range_minutes": 10,
    
    # 时间间隔
    "interval": "10s",
    
    # 聚合方式
    "aggregation": "last",
    
    # 填充方式
    "fill": "null"
}

# 分页配置
PAGINATION_CONFIG = {
    # 默认页码
    "page_num": 1,
    
    # 默认每页数量
    "page_size": 10
} 