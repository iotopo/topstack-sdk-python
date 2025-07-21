#!/usr/bin/env python3
"""
TopStack Python SDK 连接诊断脚本

这个脚本会详细诊断连接问题，帮助您找出具体的错误原因
"""

import sys
import os
import requests
import json
from datetime import datetime

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_connectivity():
    """测试基本连接"""
    print("=== 基本连接测试 ===")
    
    try:
        from config import TOPSTACK_CONFIG
        
        base_url = TOPSTACK_CONFIG["base_url"]
        print(f"测试连接: {base_url}")
        
        # 测试基本 HTTP 连接
        response = requests.get(base_url, timeout=10, verify=False)
        print(f"✓ HTTP 连接成功，状态码: {response.status_code}")
        
        # 测试 API 端点
        api_url = f"{base_url}/alert/open_api/v1/alert_level"
        print(f"测试 API 端点: {api_url}")
        
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': TOPSTACK_CONFIG["api_key"],
            'x-ProjectID': TOPSTACK_CONFIG["project_id"],
        }
        
        response = requests.get(api_url, headers=headers, timeout=10, verify=False)
        print(f"✓ API 端点响应，状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✓ 响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"⚠ 响应不是有效的 JSON: {response.text[:200]}")
        else:
            print(f"✗ API 端点返回错误状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
        
        return True
        
    except requests.exceptions.ConnectionError as e:
        print(f"✗ 连接错误: {e}")
        print("可能的原因:")
        print("1. TopStack 服务未启动")
        print("2. 端口号不正确")
        print("3. 防火墙阻止连接")
        return False
        
    except requests.exceptions.Timeout as e:
        print(f"✗ 连接超时: {e}")
        print("可能的原因:")
        print("1. 网络连接缓慢")
        print("2. 服务响应慢")
        print("3. 超时时间设置过短")
        return False
        
    except Exception as e:
        print(f"✗ 其他错误: {type(e).__name__}: {e}")
        return False

def test_sdk_connection():
    """测试 SDK 连接"""
    print("\n=== SDK 连接测试 ===")
    
    try:
        from topstack import TopStackClient
        from topstack.alert import AlertApi
        from config import TOPSTACK_CONFIG
        
        print("创建 TopStack 客户端...")
        client = TopStackClient(
            base_url=TOPSTACK_CONFIG["base_url"],
            api_key=TOPSTACK_CONFIG["api_key"],
            project_id=TOPSTACK_CONFIG["project_id"],
            timeout=TOPSTACK_CONFIG["timeout"],
            verify_ssl=TOPSTACK_CONFIG["verify_ssl"]
        )
        print("✓ 客户端创建成功")
        
        print("创建 AlertApi 实例...")
        alert_api = AlertApi(client)
        print("✓ AlertApi 创建成功")
        
        print("调用 query_alert_levels API...")
        response = alert_api.query_alert_levels()
        print("✓ API 调用成功")
        print(f"响应数据: {response.data}")
        
        return True
        
    except Exception as e:
        print(f"✗ SDK 连接失败")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        
        # 详细分析错误
        if hasattr(e, 'status_code'):
            print(f"HTTP 状态码: {e.status_code}")
        
        if hasattr(e, 'response') and e.response:
            print(f"响应对象: {e.response}")
        
        # 检查是否是认证错误
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("🔍 分析: 可能是认证错误")
            print("请检查:")
            print("1. API 密钥是否正确")
            print("2. 项目 ID 是否正确")
            print("3. API 密钥是否有权限访问该项目")
        
        # 检查是否是路径错误
        elif "404" in str(e) or "not found" in str(e).lower():
            print("🔍 分析: 可能是 API 路径错误")
            print("请检查:")
            print("1. TopStack 服务版本是否支持该 API")
            print("2. API 路径是否正确")
        
        # 检查是否是 JSON 解析错误
        elif "json" in str(e).lower() or "decode" in str(e).lower():
            print("🔍 分析: 可能是响应格式错误")
            print("请检查:")
            print("1. 服务返回的响应格式是否正确")
            print("2. 服务是否正常运行")
        
        return False

def test_configuration():
    """测试配置"""
    print("\n=== 配置测试 ===")
    
    try:
        from config import TOPSTACK_CONFIG
        
        required_keys = ["base_url", "api_key", "project_id", "timeout", "verify_ssl"]
        
        for key in required_keys:
            if key not in TOPSTACK_CONFIG:
                print(f"✗ 缺少配置项: {key}")
                return False
            else:
                value = TOPSTACK_CONFIG[key]
                if key == "api_key":
                    # 隐藏 API 密钥的详细信息
                    display_value = f"{value[:8]}..." if len(value) > 8 else "***"
                else:
                    display_value = value
                print(f"✓ {key}: {display_value}")
        
        # 验证 URL 格式
        base_url = TOPSTACK_CONFIG["base_url"]
        if not base_url.startswith(("http://", "https://")):
            print(f"✗ base_url 格式错误: {base_url}")
            print("应该以 http:// 或 https:// 开头")
            return False
        
        print("✓ 配置验证通过")
        return True
        
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False

def main():
    """主函数"""
    print("TopStack Python SDK 连接诊断")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_basic_connectivity,
        test_sdk_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"诊断结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过，连接正常！")
        return 0
    else:
        print("✗ 发现问题，请根据上述错误信息进行排查")
        print("\n常见解决方案:")
        print("1. 检查 TopStack 服务是否正在运行")
        print("2. 验证 config.py 中的配置参数")
        print("3. 确认 API 密钥和项目 ID 的正确性")
        print("4. 检查网络连接和防火墙设置")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 