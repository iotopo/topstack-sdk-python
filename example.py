"""
TopStack Python SDK 使用示例
"""

from datetime import datetime, timedelta
from topstack import TopStackClient
from topstack.iot import IotApi, DeviceApi
from topstack.alert import AlertApi
from topstack.asset import AssetApi
from topstack.ems import EmsApi
from topstack.datav import DatavApi

def main():
    """主函数"""
    # 初始化客户端
    api_key = "8mphozy98fkor6iu"
    project_id = "iotopo"
    client = TopStackClient(
        base_url="http://localhost:8000",
        api_key=api_key,
        project_id=project_id
    )
    
    # 创建各个 API 实例
    iot_api = IotApi(client)
    device_api = DeviceApi(client)
    alert_api = AlertApi(client)
    asset_api = AssetApi(client)
    ems_api = EmsApi(client)
    datav_api = DatavApi(client)
    
    # 示例 1: 查询告警级别
    try:
        alert_levels = alert_api.query_alert_levels()
        print("告警级别:", alert_levels.data)
    except Exception as e:
        print(f"查询告警级别失败: {e}")
    
    # 示例 2: 查询单测点实时值
    try:
        response = iot_api.find_last(device_id="dev1", point_id="v1")
        print(f"{response.device_id}.{response.point_id}={response.value}({response.timestamp})")
    except Exception as e:
        print(f"查询单测点实时值失败: {e}")
    
    # 示例 3: 批量查询多测点实时值
    try:
        batch_response = iot_api.find_last_batch([
            {"device_id": "dev1", "point_id": "v1"},
            {"device_id": "dev2", "point_id": "v2"}
        ])
        print("批量查询结果:", batch_response)
    except Exception as e:
        print(f"批量查询失败: {e}")
    
    # 示例 4: 控制指令下发
    try:
        iot_api.set_value(device_id="dev1", point_id="V4", value="2")
        print("控制指令下发成功")
    except Exception as e:
        print(f"控制指令下发失败: {e}")
    
    # 示例 5: 查询历史数据
    try:
        history_response = iot_api.query_history(
            points=[{"device_id": "dev1", "point_id": "v1"}],
            start=datetime.now() - timedelta(minutes=10),
            end=datetime.now(),
            interval="10s",
            aggregation="last"
        )
        print("历史数据查询成功:", len(history_response.results))
    except Exception as e:
        print(f"查询历史数据失败: {e}")
    
    # 示例 6: 查询设备
    try:
        devices = device_api.query(search="dev1", page_num=1, page_size=10)
        print("设备查询成功:", len(devices.items))
    except Exception as e:
        print(f"查询设备失败: {e}")
    
    # 示例 7: 查询设备属性
    try:
        props = device_api.query_props("dev1")
        print("设备属性查询成功:", len(props))
    except Exception as e:
        print(f"查询设备属性失败: {e}")
    
    # 示例 8: 查询工单
    try:
        work_orders = asset_api.query_work_orders(search="", page_num=1, page_size=10)
        print("工单查询成功:", work_orders.data)
    except Exception as e:
        print(f"查询工单失败: {e}")
    
    # 示例 9: 获取数据可视化页面 URL
    try:
        page_url = datav_api.get_page_url(
            base_url="http://localhost:8000",
            page_id="ct9avosgj6lmas2l2hl0",
            token="8061337fe3e34be1bf0ee1a4e15d3a63"
        )
        print("数据可视化页面 URL:", page_url)
    except Exception as e:
        print(f"获取页面 URL 失败: {e}")

if __name__ == "__main__":
    main() 