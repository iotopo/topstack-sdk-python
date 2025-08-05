#!/usr/bin/env python3
"""
NATS 模块测试
"""

import json
import asyncio
from datetime import datetime
from src.topstack_sdk.nats import (
    NatsConfig, 
    PointData, 
    DeviceState, 
    GatewayState, 
    ChannelState, 
    AlertInfo
)


def test_point_data():
    """测试 PointData 类"""
    print("=== 测试 PointData 类 ===")
    
    # 创建测试数据
    test_data = {
        "deviceID": "device_001",
        "pointID": "point_001",
        "value": 25.5,
        "quality": 1,
        "timestamp": "2024-01-01T12:00:00Z",
        "status": 0,
        "deviceTypeID": "type_001",
        "projectID": "project_001",
        "gatewayID": "gateway_001",
        "notSave": False
    }
    
    # 从字典创建对象
    point_data = PointData.from_dict(test_data)
    
    print(f"设备ID: {point_data.device_id}")
    print(f"测点ID: {point_data.point_id}")
    print(f"值: {point_data.value}")
    print(f"质量: {point_data.quality}")
    print(f"时间戳: {point_data.timestamp}")
    print(f"状态: {point_data.status}")
    print()


def test_device_state():
    """测试 DeviceState 类"""
    print("=== 测试 DeviceState 类 ===")
    
    # 创建测试数据
    test_data = {
        "projectID": "project_001",
        "gatewayID": "gateway_001",
        "deviceID": "device_001",
        "state": 1,
        "timestamp": "2024-01-01T12:00:00Z"
    }
    
    # 从字典创建对象
    device_state = DeviceState.from_dict(test_data)
    
    print(f"项目ID: {device_state.project_id}")
    print(f"网关ID: {device_state.gateway_id}")
    print(f"设备ID: {device_state.device_id}")
    print(f"状态: {device_state.state}")
    print(f"时间戳: {device_state.timestamp}")
    print()


def test_gateway_state():
    """测试 GatewayState 类"""
    print("=== 测试 GatewayState 类 ===")
    
    # 创建测试数据
    test_data = {
        "sn": "GW001",
        "name": "网关1",
        "projectID": "project_001",
        "gatewayID": "gateway_001",
        "state": 1,
        "timestamp": "2024-01-01T12:00:00Z"
    }
    
    # 从字典创建对象
    gateway_state = GatewayState.from_dict(test_data)
    
    print(f"序列号: {gateway_state.sn}")
    print(f"名称: {gateway_state.name}")
    print(f"项目ID: {gateway_state.project_id}")
    print(f"网关ID: {gateway_state.gateway_id}")
    print(f"状态: {gateway_state.state}")
    print(f"时间戳: {gateway_state.timestamp}")
    print()


def test_channel_state():
    """测试 ChannelState 类"""
    print("=== 测试 ChannelState 类 ===")
    
    # 创建测试数据
    test_data = {
        "projectID": "project_001",
        "gatewayID": "gateway_001",
        "channelID": "channel_001",
        "running": True,
        "connected": True,
        "timestamp": "2024-01-01T12:00:00Z",
        "gatewayName": "网关1",
        "channelName": "通道1"
    }
    
    # 从字典创建对象
    channel_state = ChannelState.from_dict(test_data)
    
    print(f"项目ID: {channel_state.project_id}")
    print(f"网关ID: {channel_state.gateway_id}")
    print(f"通道ID: {channel_state.channel_id}")
    print(f"运行状态: {channel_state.running}")
    print(f"连接状态: {channel_state.connected}")
    print(f"时间戳: {channel_state.timestamp}")
    print(f"网关名称: {channel_state.gateway_name}")
    print(f"通道名称: {channel_state.channel_name}")
    print()


def test_alert_info():
    """测试 AlertInfo 类"""
    print("=== 测试 AlertInfo 类 ===")
    
    # 创建测试数据
    test_data = {
        "id": "alert_001",
        "status": "unhandled",
        "createdAt": "2024-01-01T12:00:00Z",
        "title": "温度过高告警",
        "content": "设备温度超过阈值",
        "projectID": "project_001",
        "deviceID": "device_001",
        "alertTypeID": "type_001",
        "alertLevelID": "level_001",
        "ruleName": "温度监控规则",
        "alertTypeName": "温度告警",
        "alertTypeCode": "TEMP_ALERT",
        "alertLevelCode": "HIGH",
        "alertLevelColor": "#FF0000",
        "alertLevelName": "高级",
        "deviceName": "温度传感器1",
        "pointName": "温度",
        "deviceTypeID": "type_001",
        "deviceGroupID": "group_001",
        "deviceAttr": {"location": "车间A"}
    }
    
    # 从字典创建对象
    alert_info = AlertInfo.from_dict(test_data)
    
    print(f"告警ID: {alert_info.alert_id}")
    print(f"状态: {alert_info.status}")
    print(f"创建时间: {alert_info.created_at}")
    print(f"标题: {alert_info.title}")
    print(f"内容: {alert_info.content}")
    print(f"项目ID: {alert_info.project_id}")
    print(f"设备ID: {alert_info.device_id}")
    print(f"告警类型ID: {alert_info.alert_type_id}")
    print(f"告警等级ID: {alert_info.alert_level_id}")
    print(f"规则名称: {alert_info.rule_name}")
    print(f"告警类型名称: {alert_info.alert_type_name}")
    print(f"告警类型代码: {alert_info.alert_type_code}")
    print(f"告警等级代码: {alert_info.alert_level_code}")
    print(f"告警等级颜色: {alert_info.alert_level_color}")
    print(f"告警等级名称: {alert_info.alert_level_name}")
    print(f"设备名称: {alert_info.device_name}")
    print(f"测点名称: {alert_info.point_name}")
    print(f"设备类型ID: {alert_info.device_type_id}")
    print(f"设备组ID: {alert_info.device_group_id}")
    print(f"设备属性: {alert_info.device_attr}")
    print()


def test_nats_config():
    """测试 NatsConfig 类"""
    print("=== 测试 NatsConfig 类 ===")
    
    config = NatsConfig(
        addr="nats://localhost:4222",
        token="test_token",
        username="test_user",
        password="test_pass"
    )
    
    print(f"地址: {config.addr}")
    print(f"令牌: {config.token}")
    print(f"用户名: {config.username}")
    print(f"密码: {config.password}")
    print()


def main():
    """主测试函数"""
    print("开始测试 NATS 模块...\n")
    
    test_nats_config()
    test_point_data()
    test_device_state()
    test_gateway_state()
    test_channel_state()
    test_alert_info()
    
    print("所有测试完成！")


if __name__ == "__main__":
    main() 