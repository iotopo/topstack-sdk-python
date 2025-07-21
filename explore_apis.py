#!/usr/bin/env python3
"""
TopStack API 探索脚本

这个脚本会尝试不同的 API 端点，找出您的 TopStack 服务支持哪些 API
"""

import sys
import os
import requests
import json
from urllib.parse import urljoin

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_endpoint(base_url, endpoint, method="GET", headers=None, data=None):
    """测试单个 API 端点"""
    url = urljoin(base_url, endpoint)
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=10, verify=False)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
        else:
            print(f"不支持的方法: {method}")
            return None
        
        return {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "content": response.text[:500] if response.text else "",
            "headers": dict(response.headers)
        }
    except Exception as e:
        return {
            "url": url,
            "method": method,
            "error": str(e)
        }

def explore_apis():
    """探索 API 端点"""
    print("TopStack API 探索")
    print("=" * 50)
    
    try:
        from config import TOPSTACK_CONFIG
        base_url = TOPSTACK_CONFIG["base_url"]
        api_key = TOPSTACK_CONFIG["api_key"]
        project_id = TOPSTACK_CONFIG["project_id"]
        
        print(f"基础 URL: {base_url}")
        print(f"项目 ID: {project_id}")
        print()
        
        # 设置请求头
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': api_key,
            'x-ProjectID': project_id,
        }
        
        # 常见的 API 端点列表
        api_endpoints = [
            # 基础端点
            ("/", "GET"),
            ("/api", "GET"),
            ("/api/v1", "GET"),
            ("/open_api", "GET"),
            ("/open_api/v1", "GET"),
            
            # 告警相关 - 使用正确的端点
            ("/alert/open_api/v1/alert_level", "GET"),
            ("/alert/open_api/v1/alert_type", "GET"),
            ("/alert/open_api/v1/alert_record", "GET"),
            ("/alert/open_api/v1/alert_record/activity", "GET"),
            
            # IoT 相关
            ("/iot/open_api/v1/data/findLast", "POST"),
            ("/iot/open_api/v1/data/findLastBatch", "POST"),
            ("/iot/open_api/v1/data/setValue", "POST"),
            ("/iot/open_api/v1/data/query", "POST"),
            ("/iot/open_api/v1/device/query", "GET"),
            ("/iot/open_api/v1/device/points", "GET"),
            ("/iot/open_api/v1/device_type/query", "GET"),
            ("/iot/open_api/v1/device_group/all", "GET"),
            ("/iot/open_api/v1/gateway/query", "GET"),
            
            # 资产管理 - 使用正确的端点
            ("/asset/open_api/v1/alert_work_order", "GET"),
            ("/asset/open_api/v1/locale_work_order", "GET"),
            ("/asset/open_api/v1/maintenance_work_order", "GET"),
            ("/asset/open_api/v1/schedule_work_order", "GET"),
            
            # 能源管理
            ("/ems/open_api/v1/meter/query", "POST"),
            ("/ems/open_api/v1/sector/query", "POST"),
            ("/ems/open_api/v1/subentry/query", "POST"),
            ("/ems/open_api/v1/report/meter/hourly", "GET"),
            ("/ems/open_api/v1/report/sector/hourly", "GET"),
            ("/ems/open_api/v1/report/subentry/hourly", "GET"),
            
            # 全局变量
            ("/open_api/v1/global_var/get_value", "GET"),
            ("/open_api/v1/global_var/update_value", "POST"),
        ]
        
        print("正在测试 API 端点...")
        print()
        
        working_endpoints = []
        failed_endpoints = []
        
        for endpoint, method in api_endpoints:
            print(f"测试: {method} {endpoint}")
            
            # 对于 POST 请求，添加一些测试数据
            data = None
            if method == "POST":
                if "findLast" in endpoint:
                    data = {"deviceID": "test", "pointID": "test"}
                elif "query" in endpoint:
                    data = {"pageNum": 1, "pageSize": 10}
                elif "setValue" in endpoint:
                    data = {"deviceID": "test", "pointID": "test", "value": "0"}
            
            result = test_api_endpoint(base_url, endpoint, method, headers, data)
            
            if result:
                if "error" in result:
                    print(f"  ✗ 错误: {result['error']}")
                    failed_endpoints.append((endpoint, method, result['error']))
                elif result['status_code'] == 200:
                    print(f"  ✓ 成功 (200)")
                    working_endpoints.append((endpoint, method, result))
                elif result['status_code'] == 401:
                    print(f"  ⚠ 认证失败 (401) - 可能需要正确的认证信息")
                    failed_endpoints.append((endpoint, method, "认证失败"))
                elif result['status_code'] == 404:
                    print(f"  ✗ 不存在 (404)")
                    failed_endpoints.append((endpoint, method, "端点不存在"))
                else:
                    print(f"  ⚠ 其他状态码: {result['status_code']}")
                    if result['content']:
                        print(f"    响应: {result['content'][:100]}...")
                    failed_endpoints.append((endpoint, method, f"状态码 {result['status_code']}"))
            else:
                print(f"  ✗ 测试失败")
                failed_endpoints.append((endpoint, method, "测试失败"))
            
            print()
        
        # 总结结果
        print("=" * 50)
        print("探索结果总结")
        print("=" * 50)
        
        if working_endpoints:
            print(f"\n✓ 可用的 API 端点 ({len(working_endpoints)} 个):")
            for endpoint, method, result in working_endpoints:
                print(f"  {method} {endpoint}")
                if result.get('content'):
                    print(f"    响应示例: {result['content'][:100]}...")
                print()
        
        if failed_endpoints:
            print(f"\n✗ 不可用的 API 端点 ({len(failed_endpoints)} 个):")
            for endpoint, method, error in failed_endpoints:
                print(f"  {method} {endpoint} - {error}")
        
        print(f"\n总计测试了 {len(api_endpoints)} 个 API 端点")
        print(f"可用: {len(working_endpoints)} 个")
        print(f"不可用: {len(failed_endpoints)} 个")
        
        # 提供建议
        if working_endpoints:
            print("\n💡 建议:")
            print("1. 根据可用的 API 端点调整 SDK 代码")
            print("2. 检查 TopStack 服务的 API 文档")
            print("3. 确认 API 版本和路径格式")
        else:
            print("\n⚠ 警告:")
            print("1. 没有找到可用的 API 端点")
            print("2. 请检查 TopStack 服务是否正确启动")
            print("3. 确认 API 密钥和项目 ID 是否正确")
            print("4. 查看 TopStack 服务的日志")
        
        return len(working_endpoints) > 0
        
    except Exception as e:
        print(f"探索过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    success = explore_apis()
    sys.exit(0 if success else 1) 