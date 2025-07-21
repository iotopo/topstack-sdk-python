#!/usr/bin/env python3
"""
TopStack Python SDK 示例脚本
"""

import sys
import os
import time
from datetime import datetime, timedelta

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """检查依赖是否已安装"""
    try:
        import requests
        import pydantic
        print("✓ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"✗ 依赖检查失败: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_sdk_import():
    """检查 SDK 是否可以正常导入"""
    try:
        from topstack_sdk import TopStackClient, IotApi, DeviceApi, AlertApi, AssetApi, EmsApi, DatavApi
        print("✓ SDK 导入成功")
        return True
    except ImportError as e:
        print(f"✗ SDK 导入失败: {e}")
        return False

def create_client():
    """创建 TopStack 客户端"""
    try:
        # 导入配置
        from config import TOPSTACK_CONFIG
        
        print(f"正在连接到 TopStack 服务: {TOPSTACK_CONFIG['base_url']}")
        print(f"项目 ID: {TOPSTACK_CONFIG['project_id']}")
        
        client = TopStackClient(
            base_url=TOPSTACK_CONFIG["base_url"],
            api_key=TOPSTACK_CONFIG["api_key"],
            project_id=TOPSTACK_CONFIG["project_id"],
            timeout=TOPSTACK_CONFIG["timeout"],
            verify_ssl=TOPSTACK_CONFIG["verify_ssl"]
        )
        print("✓ 客户端创建成功")
        return client
    except ImportError:
        print("✗ 配置文件导入失败，请检查 config.py 文件")
        return None
    except Exception as e:
        print(f"✗ 客户端创建失败: {e}")
        return None

def test_connection(client):
    """测试连接"""
    print("\n=== 测试连接 ===")
    try:
        # 尝试一个简单的 API 调用 - 使用告警 API
        from topstack_sdk.alert import AlertApi
        alert_api = AlertApi(client)
        
        # 使用告警级别查询来测试连接
        response = alert_api.query_alert_levels()
        print("✓ 连接测试成功")
        return True
    except Exception as e:
        print(f"✗ 连接测试失败: {e}")
        print("请检查:")
        print("1. TopStack 服务是否正在运行")
        print("2. API 密钥和项目 ID 是否正确")
        print("3. 网络连接是否正常")
        return False

def demo_iot_operations(client):
    """演示 IoT 操作"""
    print("\n=== IoT 操作演示 ===")
    
    from topstack_sdk.iot import IotApi
    
    iot_api = IotApi(client)
    
    # 导入测试设备配置
    from config import TEST_DEVICES
    
    test_device = TEST_DEVICES["device_id"]
    test_point = TEST_DEVICES["point_id"]
    
    print(f"使用测试设备: {test_device}, 测点: {test_point}")
    
    # 1. 查询单测点实时值
    print("\n1. 查询单测点实时值...")
    try:
        # 使用正确的字段名
        request_data = {"deviceID": test_device, "pointID": test_point}
        response = client.post("/iot/open_api/v1/data/findLast", request_data)
        print("✓ 查询成功")
        if response.data:
            print(f"  响应数据: {response.data}")
    except Exception as e:
        print(f"✗ 查询失败: {e}")
    
    # 2. 批量查询多测点实时值
    print("\n2. 批量查询多测点实时值...")
    try:
        # 使用正确的字段名
        batch_data = [
            {"deviceID": test_device, "pointID": test_point},
            {"deviceID": "dev2", "pointID": "v2"}
        ]
        batch_response = client.post("/iot/open_api/v1/data/findLastBatch", batch_data)
        print("✓ 批量查询成功")
        if batch_response.data:
            print(f"  响应数据: {batch_response.data}")
    except Exception as e:
        print(f"✗ 批量查询失败: {e}")
    
    # 3. 控制指令下发
    print("\n3. 控制指令下发...")
    try:
        # 使用正确的字段名
        control_data = {
            "deviceID": test_device, 
            "pointID": "V4",  # 使用配置中的控制点
            "value": "2"
        }
        response = client.post("/iot/open_api/v1/data/setValue", control_data)
        print("✓ 控制指令下发成功")
        if response.data:
            print(f"  响应数据: {response.data}")
    except Exception as e:
        print(f"✗ 控制指令下发失败: {e}")
    
    # 4. 查询历史数据
    print("\n4. 查询历史数据...")
    try:
        from config import HISTORY_CONFIG
        
        # 使用正确的字段名和时间格式
        from datetime import timezone
        start_time = datetime.now(timezone.utc) - timedelta(minutes=HISTORY_CONFIG["time_range_minutes"])
        end_time = datetime.now(timezone.utc)
        
        history_data = {
            "points": [{"deviceID": test_device, "pointID": test_point}],
            "start": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "interval": HISTORY_CONFIG["interval"],
            "aggregation": HISTORY_CONFIG["aggregation"]
        }
        history_response = client.post("/iot/open_api/v1/data/query", history_data)
        print("✓ 历史数据查询成功")
        if history_response.data:
            print(f"  响应数据: {history_response.data}")
    except Exception as e:
        print(f"✗ 历史数据查询失败: {e}")

def demo_device_operations(client):
    """演示设备管理操作"""
    print("\n=== 设备管理操作演示 ===")
    
    from topstack_sdk.iot import DeviceApi
    
    device_api = DeviceApi(client)
    
    # 1. 查询设备
    print("\n1. 查询设备...")
    try:
        from config import PAGINATION_CONFIG
        devices = device_api.query(search="", page_num=PAGINATION_CONFIG["page_num"], page_size=PAGINATION_CONFIG["page_size"])
        print(f"✓ 设备查询成功，共 {devices.total} 个设备")
        for device in devices.items[:3]:  # 只显示前3个
            print(f"  {device.name} ({device.id}) - 状态: {'在线' if device.state == 0 else '离线'}")
    except Exception as e:
        print(f"✗ 设备查询失败: {e}")
    
    # 2. 查询设备属性
    print("\n2. 查询设备属性...")
    try:
        # 使用配置中的设备ID
        from config import TEST_DEVICES
        props = device_api.query_props(TEST_DEVICES["device_id"])
        print(f"✓ 设备属性查询成功，共 {len(props)} 个属性")
        for prop in props[:3]:  # 只显示前3个
            print(f"  {prop.name} ({prop.property_type}): {prop.value}")
    except Exception as e:
        print(f"✗ 设备属性查询失败: {e}")

def demo_alert_operations(client):
    """演示告警操作"""
    print("\n=== 告警操作演示 ===")
    
    from topstack_sdk.alert import AlertApi
    
    alert_api = AlertApi(client)
    
    # 1. 查询告警级别
    print("\n1. 查询告警级别...")
    try:
        alert_levels = alert_api.query_alert_levels()
        print("✓ 告警级别查询成功")
        if alert_levels.data:
            print(f"  返回 {len(alert_levels.data)} 个告警级别")
            for level in alert_levels.data[:3]:  # 只显示前3个
                if isinstance(level, dict):
                    print(f"    {level.get('name', 'N/A')} ({level.get('code', 'N/A')}) - 颜色: {level.get('color', 'N/A')}")
                else:
                    print(f"    {level}")
    except Exception as e:
        print(f"✗ 告警级别查询失败: {e}")
    
    # 2. 查询告警类型
    print("\n2. 查询告警类型...")
    try:
        alert_types = alert_api.query_alert_types()
        print("✓ 告警类型查询成功")
        if alert_types.data and hasattr(alert_types.data, 'types'):
            print(f"  返回 {len(alert_types.data.types)} 个告警类型")
            for alert_type in alert_types.data.types[:3]:  # 只显示前3个
                print(f"    {alert_type.name} ({alert_type.code})")
    except Exception as e:
        print(f"✗ 告警类型查询失败: {e}")
    
    # 3. 查询告警记录
    print("\n3. 查询告警记录...")
    try:
        from datetime import datetime, timedelta
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        alert_records = alert_api.query_alert_records(
            start=start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end=end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            pageNum=1,
            pageSize=5
        )
        print("✓ 告警记录查询成功")
        if alert_records.data and hasattr(alert_records.data, 'records'):
            print(f"  返回 {len(alert_records.data.records)} 条告警记录")
    except Exception as e:
        print(f"✗ 告警记录查询失败: {e}")

def demo_asset_operations(client):
    """演示资产管理操作"""
    print("\n=== 资产管理操作演示 ===")
    
    from topstack_sdk.asset import AssetApi
    
    asset_api = AssetApi(client)
    
    # 1. 查询告警工单
    print("\n1. 查询告警工单...")
    try:
        work_orders = asset_api.query_work_orders(pageSize=5, pageNum=1)
        print("✓ 告警工单查询成功")
        if work_orders.data and hasattr(work_orders.data, 'items'):
            print(f"  返回 {len(work_orders.data.items)} 个工单")
            for order in work_orders.data.items[:3]:  # 只显示前3个
                print(f"    工单 {order.code} - 状态: {order.status}")
    except Exception as e:
        print(f"✗ 告警工单查询失败: {e}")
    
    # 2. 查询现场工单
    print("\n2. 查询现场工单...")
    try:
        locale_orders = client.get("/asset/open_api/v1/locale_work_order", {"pageSize": 5, "pageNum": 1})
        print("✓ 现场工单查询成功")
        if locale_orders.data:
            print(f"  返回 {len(locale_orders.data)} 个工单")
    except Exception as e:
        print(f"✗ 现场工单查询失败: {e}")
    
    # 3. 查询维护工单
    print("\n3. 查询维护工单...")
    try:
        maintenance_orders = client.get("/asset/open_api/v1/maintenance_work_order", {"pageSize": 5, "pageNum": 1})
        print("✓ 维护工单查询成功")
        if maintenance_orders.data:
            print(f"  返回 {len(maintenance_orders.data)} 个工单")
    except Exception as e:
        print(f"✗ 维护工单查询失败: {e}")

def demo_datav_operations(client):
    """演示数据可视化操作"""
    print("\n=== 数据可视化操作演示 ===")
    
    from topstack_sdk.datav import DatavApi
    
    datav_api = DatavApi(client)
    
    # 生成页面 URL
    print("\n1. 生成数据可视化页面 URL...")
    try:
        from config import DATAV_CONFIG, TOPSTACK_CONFIG
        
        page_url = datav_api.get_page_url(
            base_url=TOPSTACK_CONFIG["base_url"],
            page_id=DATAV_CONFIG["page_id"],
            token=DATAV_CONFIG["token"],
            username=DATAV_CONFIG["username"],
            password=DATAV_CONFIG["password"]
        )
        print("✓ 页面 URL 生成成功")
        print(f"  URL: {page_url}")
    except Exception as e:
        print(f"✗ 页面 URL 生成失败: {e}")

def main():
    """主函数"""
    from config import TOPSTACK_CONFIG
    print("TopStack Python SDK 运行示例")
    print("==================================================")
    print(f"服务地址: {TOPSTACK_CONFIG['base_url']}")
    print(f"API Key: {TOPSTACK_CONFIG['api_key']}")
    print(f"项目 ID: {TOPSTACK_CONFIG['project_id']}")

    # 必须在此处导入 TopStackClient，确保作用域可见
    from topstack_sdk import TopStackClient

    try:
        client = TopStackClient(
            base_url=TOPSTACK_CONFIG["base_url"],
            api_key=TOPSTACK_CONFIG["api_key"],
            project_id=TOPSTACK_CONFIG["project_id"]
        )
    except Exception as e:
        print(f"✗ 客户端创建失败: {e}")
        return

    # 测试连接
    if not test_connection(client):
        return 1
    
    # 运行各种演示
    try:
        demo_iot_operations(client)
        demo_device_operations(client)
        demo_alert_operations(client)
        demo_asset_operations(client)
        demo_datav_operations(client)
        
        print("\n" + "=" * 50)
        print("✓ 所有演示完成！")
        print("\n提示:")
        print("- 如果某些操作失败，请检查相应的设备、测点是否存在")
        print("- 可以根据实际环境修改配置信息")
        print("- 更多用法请参考 example.py 和 README.md")
        
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n✗ 运行过程中发生错误: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    check_sdk_import()
    exit_code = main()
    sys.exit(exit_code) 