"""
TopStack SDK 基本使用示例
"""

from topstack_sdk import TopStackClient
from topstack_sdk.iot import IotApi
from topstack_sdk.alert import AlertApi
from topstack_sdk.asset import AssetApi


def main():
    """基本使用示例"""
    
    # 1. 创建客户端
    client = TopStackClient(
        base_url="http://localhost:8000",
        api_key="your-api-key",
        project_id="your-project-id"
    )
    
    print("=== TopStack SDK 基本使用示例 ===")
    
    # 2. 使用 IoT API
    print("\n--- IoT 操作 ---")
    iot_api = IotApi(client)
    
    try:
        # 查询单点实时数据
        data = iot_api.find_last("dev1", "v1")
        print(f"✓ 实时数据查询成功: {data}")
    except Exception as e:
        print(f"✗ 实时数据查询失败: {e}")
    
    try:
        # 查询设备
        devices = client.get("/iot/open_api/v1/device/query")
        print(f"✓ 设备查询成功，共 {len(devices.data.items)} 个设备")
    except Exception as e:
        print(f"✗ 设备查询失败: {e}")
    
    # 3. 使用告警 API
    print("\n--- 告警操作 ---")
    alert_api = AlertApi(client)
    
    try:
        # 查询告警级别
        alert_levels = alert_api.query_alert_levels()
        print(f"✓ 告警级别查询成功，共 {len(alert_levels.data)} 个级别")
    except Exception as e:
        print(f"✗ 告警级别查询失败: {e}")
    
    try:
        # 查询告警类型
        alert_types = alert_api.query_alert_types()
        print("✓ 告警类型查询成功")
    except Exception as e:
        print(f"✗ 告警类型查询失败: {e}")
    
    # 4. 使用资产管理 API
    print("\n--- 资产管理操作 ---")
    asset_api = AssetApi(client)
    
    try:
        # 查询工单
        work_orders = asset_api.query_work_orders(pageSize=5, pageNum=1)
        print("✓ 工单查询成功")
    except Exception as e:
        print(f"✗ 工单查询失败: {e}")
    
    print("\n=== 示例完成 ===")


if __name__ == "__main__":
    main() 