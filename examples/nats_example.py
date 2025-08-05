#!/usr/bin/env python3
"""
NATS 消息总线使用示例
"""

import asyncio
import logging
from datetime import datetime
from topstack_sdk.nats import NatsConfig, create_nats_bus, PointData, DeviceState, GatewayState, ChannelState, AlertInfo


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def point_data_handler(point_data: PointData):
    """处理测点数据"""
    logger.info(f"收到测点数据: 设备={point_data.device_id}, 测点={point_data.point_id}, "
                f"值={point_data.value}, 质量={point_data.quality}, 时间={point_data.timestamp}")


async def device_state_handler(device_state: DeviceState):
    """处理设备状态数据"""
    status = "在线" if device_state.state == 1 else "离线"
    logger.info(f"设备状态变化: 设备={device_state.device_id}, 状态={status}, 时间={device_state.timestamp}")


async def gateway_state_handler(gateway_state: GatewayState):
    """处理网关状态数据"""
    status = "在线" if gateway_state.state == 1 else "离线"
    logger.info(f"网关状态变化: 网关={gateway_state.gateway_id}, 状态={status}, 时间={gateway_state.timestamp}")


async def channel_state_handler(channel_state: ChannelState):
    """处理数据通道状态数据"""
    running = "运行中" if channel_state.running else "已停止"
    connected = "已连接" if channel_state.connected else "未连接"
    logger.info(f"数据通道状态: 通道={channel_state.channel_id}, 运行={running}, "
                f"连接={connected}, 时间={channel_state.timestamp}")


async def alert_info_handler(alert_info: AlertInfo):
    """处理告警信息"""
    logger.info(f"收到告警: ID={alert_info.alert_id}, 标题={alert_info.title}, "
                f"状态={alert_info.status}, 时间={alert_info.created_at}")


async def main():
    """主函数"""
    # 创建 NATS 配置
    config = NatsConfig(
        addr="nats://localhost:4222",  # NATS 服务器地址
        token="your_token_here",       # 认证令牌（可选）
        username="your_username",       # 用户名（可选）
        password="your_password"        # 密码（可选）
    )
    
    try:
        # 创建 NATS 总线实例
        nats_bus = await create_nats_bus(config)
        logger.info("NATS 连接已建立")
        
        # 项目ID和设备ID（请根据实际情况修改）
        # project_id = "your_project_id"
        # device_id = "your_device_id"
        # device_type_id = "your_device_type_id"
        # point_id = "your_point_id"
        project_id = "*"
        device_id = "*"
        device_type_id = "*"
        point_id = "*"
        
        # 订阅设备测点数据
        point_sub = await nats_bus.subscribe_point_data(
            project_id, device_id, point_id, point_data_handler
        )
        logger.info(f"已订阅设备测点数据: {device_id}.{point_id}")
        
        # 订阅同设备模型下的测点数据
        device_type_sub = await nats_bus.subscribe_device_type_data(
            project_id, device_type_id, point_id, point_data_handler
        )
        logger.info(f"已订阅设备模型测点数据: {device_type_id}.{point_id}")
        
        # 订阅设备状态数据
        device_state_sub = await nats_bus.subscribe_device_state(
            project_id, device_id, device_state_handler
        )
        logger.info(f"已订阅设备状态: {device_id}")
        
        # 订阅网关状态数据
        gateway_state_sub = await nats_bus.subscribe_gateway_state(
            project_id, gateway_state_handler
        )
        logger.info("已订阅网关状态")
        
        # 订阅数据通道状态数据
        channel_state_sub = await nats_bus.subscribe_channel_state(
            project_id, channel_state_handler
        )
        logger.info("已订阅数据通道状态")
        
        # 订阅全部告警消息
        alert_sub = await nats_bus.subscribe_alert_info(
            project_id, alert_info_handler
        )
        logger.info("已订阅全部告警消息")
        
        # 订阅设备告警信息
        device_alert_sub = await nats_bus.subscribe_device_alert_info(
            project_id, device_id, alert_info_handler
        )
        logger.info(f"已订阅设备告警: {device_id}")
        
        # 保持连接运行
        logger.info("NATS 订阅已启动，按 Ctrl+C 退出...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("正在关闭连接...")
        
        # 取消订阅
        await point_sub.unsubscribe()
        await device_type_sub.unsubscribe()
        await device_state_sub.unsubscribe()
        await gateway_state_sub.unsubscribe()
        await channel_state_sub.unsubscribe()
        await alert_sub.unsubscribe()
        await device_alert_sub.unsubscribe()
        
        # 关闭连接
        await nats_bus.close()
        logger.info("NATS 连接已关闭")
        
    except Exception as e:
        logger.error(f"NATS 连接错误: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 