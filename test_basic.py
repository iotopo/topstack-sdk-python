#!/usr/bin/env python3
"""
TopStack Python SDK 基本功能测试

这个脚本测试 SDK 的基本功能，不需要实际连接到 TopStack 服务
"""

import sys
import os
from datetime import datetime, timedelta

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    print("=== 测试模块导入 ===")
    
    try:
        from topstack import TopStackClient, IotApi, DeviceApi, AlertApi, AssetApi, EmsApi, DatavApi
        print("✓ 所有 API 类导入成功")
        
        from topstack.iot.models import FindLastRequest, FindLastResponse, SetValueRequest
        print("✓ IoT 模型导入成功")
        
        from topstack.iot.device.models import QueryRequest, DeviceItem, PropertyItem
        print("✓ 设备管理模型导入成功")
        
        from config import TOPSTACK_CONFIG, TEST_DEVICES, DATAV_CONFIG
        print("✓ 配置文件导入成功")
        
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_client_creation():
    """测试客户端创建"""
    print("\n=== 测试客户端创建 ===")
    
    try:
        from topstack import TopStackClient
        from config import TOPSTACK_CONFIG
        
        client = TopStackClient(
            base_url=TOPSTACK_CONFIG["base_url"],
            app_id=TOPSTACK_CONFIG["app_id"],
            app_secret=TOPSTACK_CONFIG["app_secret"],
            timeout=TOPSTACK_CONFIG["timeout"],
            verify_ssl=TOPSTACK_CONFIG["verify_ssl"]
        )
        
        print("✓ 客户端创建成功")
        print(f"  基础 URL: {client.base_url}")
        print(f"  应用 ID: {client.app_id}")
        print(f"  超时时间: {client.timeout}秒")
        
        return True
    except Exception as e:
        print(f"✗ 客户端创建失败: {e}")
        return False

def test_model_creation():
    """测试数据模型创建"""
    print("\n=== 测试数据模型创建 ===")
    
    try:
        from topstack.iot.models import FindLastRequest, FindLastResponse, SetValueRequest
        from datetime import datetime
        
        # 测试请求模型 - 使用别名字段
        request = FindLastRequest(deviceID="test_dev", pointID="test_point")
        print("✓ FindLastRequest 创建成功")
        print(f"  设备ID: {request.device_id}, 测点ID: {request.point_id}")
        
        # 测试响应模型 - 使用别名字段
        response = FindLastResponse(
            deviceID="test_dev",
            pointID="test_point",
            value=25.5,
            quality=0,
            timestamp=datetime.now()
        )
        print("✓ FindLastResponse 创建成功")
        print(f"  值: {response.value}, 质量: {response.quality}")
        
        # 测试设置值请求 - 使用别名字段
        set_request = SetValueRequest(deviceID="test_dev", pointID="test_point", value="100")
        print("✓ SetValueRequest 创建成功")
        print(f"  设置值: {set_request.value}")
        
        return True
    except Exception as e:
        print(f"✗ 数据模型创建失败: {e}")
        return False

def test_device_models():
    """测试设备管理模型"""
    print("\n=== 测试设备管理模型 ===")
    
    try:
        from topstack.iot.device.models import QueryRequest, DeviceItem, PropertyItem
        from datetime import datetime
        
        # 测试查询请求
        query_req = QueryRequest(
            search="test",
            page_num=1,
            page_size=10
        )
        print("✓ QueryRequest 创建成功")
        print(f"  搜索: {query_req.search}, 页码: {query_req.page_num}")
        
        # 测试设备项 - 使用别名字段
        device = DeviceItem(
            id="dev1",
            code="DEV001",
            name="测试设备",
            connectMode="gateway",
            state=0
        )
        print("✓ DeviceItem 创建成功")
        print(f"  设备名称: {device.name}, 状态: {'在线' if device.state == 0 else '离线'}")
        
        # 测试属性项 - 使用别名字段
        prop = PropertyItem(
            id="prop1",
            type="string",
            name="测试属性",
            value="test_value"
        )
        print("✓ PropertyItem 创建成功")
        print(f"  属性名: {prop.name}, 值: {prop.value}")
        
        return True
    except Exception as e:
        print(f"✗ 设备管理模型创建失败: {e}")
        return False

def test_api_instantiation():
    """测试 API 实例化"""
    print("\n=== 测试 API 实例化 ===")
    
    try:
        from topstack import TopStackClient, IotApi, DeviceApi, AlertApi, AssetApi, EmsApi, DatavApi
        from config import TOPSTACK_CONFIG
        
        # 创建客户端
        client = TopStackClient(
            base_url=TOPSTACK_CONFIG["base_url"],
            api_key=TOPSTACK_CONFIG["api_key"],
            project_id=TOPSTACK_CONFIG["project_id"]
        )
        
        # 测试各个 API 实例化
        iot_api = IotApi(client)
        print("✓ IotApi 实例化成功")
        
        device_api = DeviceApi(client)
        print("✓ DeviceApi 实例化成功")
        
        alert_api = AlertApi(client)
        print("✓ AlertApi 实例化成功")
        
        asset_api = AssetApi(client)
        print("✓ AssetApi 实例化成功")
        
        ems_api = EmsApi(client)
        print("✓ EmsApi 实例化成功")
        
        datav_api = DatavApi(client)
        print("✓ DatavApi 实例化成功")
        
        return True
    except Exception as e:
        print(f"✗ API 实例化失败: {e}")
        return False

def test_config_validation():
    """测试配置验证"""
    print("\n=== 测试配置验证 ===")
    
    try:
        from config import TOPSTACK_CONFIG, TEST_DEVICES, DATAV_CONFIG, HISTORY_CONFIG, PAGINATION_CONFIG
        
        # 验证 TopStack 配置
        required_keys = ["base_url", "api_key", "project_id", "timeout", "verify_ssl"]
        for key in required_keys:
            if key not in TOPSTACK_CONFIG:
                raise ValueError(f"缺少配置项: {key}")
        print("✓ TopStack 配置验证通过")
        
        # 验证测试设备配置
        required_device_keys = ["device_id", "point_id", "control_point_id"]
        for key in required_device_keys:
            if key not in TEST_DEVICES:
                raise ValueError(f"缺少设备配置项: {key}")
        print("✓ 测试设备配置验证通过")
        
        # 验证数据可视化配置
        required_datav_keys = ["page_id", "token"]
        for key in required_datav_keys:
            if key not in DATAV_CONFIG:
                raise ValueError(f"缺少数据可视化配置项: {key}")
        print("✓ 数据可视化配置验证通过")
        
        return True
    except Exception as e:
        print(f"✗ 配置验证失败: {e}")
        return False

def main():
    """主函数"""
    print("TopStack Python SDK 基本功能测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_client_creation,
        test_model_creation,
        test_device_models,
        test_api_instantiation,
        test_config_validation
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
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有基本功能测试通过！")
        print("\nSDK 已准备就绪，可以运行完整示例:")
        print("- Windows: run_example.bat")
        print("- Linux/macOS: ./run_example.sh")
        print("- 直接运行: python run_example.py")
        return 0
    else:
        print("✗ 部分测试失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 