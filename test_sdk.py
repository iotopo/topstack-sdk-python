"""
TopStack Python SDK 测试文件
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from topstack import TopStackClient, TopStackError
from topstack.iot import IotApi, DeviceApi
from topstack.iot.models import FindLastRequest, FindLastResponse

class TestTopStackClient(unittest.TestCase):
    """测试 TopStack 客户端"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = TopStackClient(
            base_url="http://localhost:8000",
            api_key="test-api-key",
            project_id="test-project"
        )
    
    def test_client_initialization(self):
        """测试客户端初始化"""
        self.assertEqual(self.client.base_url, "http://localhost:8000")
        self.assertEqual(self.client.api_key, "test-api-key")
        self.assertEqual(self.client.project_id, "test-project")
        self.assertEqual(self.client.timeout, 20)
        self.assertFalse(self.client.verify_ssl)
    
    def test_client_headers(self):
        """测试客户端请求头"""
        expected_headers = {
            'Content-Type': 'application/json',
            'X-API-Key': 'test-api-key',
            'x-ProjectID': 'test-project',
        }
        self.assertEqual(self.client.session.headers, expected_headers)

class TestIotApi(unittest.TestCase):
    """测试 IoT API"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = TopStackClient(
            base_url="http://localhost:8000",
            api_key="test-api-key",
            project_id="test-project"
        )
        self.iot_api = IotApi(self.client)
    
    @patch('topstack.client.requests.Session.request')
    def test_find_last(self, mock_request):
        """测试查询单测点实时值"""
        # 模拟响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": "200",
            "msg": "success",
            "data": {
                "deviceID": "dev1",
                "pointID": "v1",
                "value": 25.5,
                "quality": 0,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        # 执行测试
        result = self.iot_api.find_last(device_id="dev1", point_id="v1")
        
        # 验证结果
        self.assertEqual(result.device_id, "dev1")
        self.assertEqual(result.point_id, "v1")
        self.assertEqual(result.value, 25.5)
        self.assertEqual(result.quality, 0)
    
    @patch('topstack.client.requests.Session.request')
    def test_set_value(self, mock_request):
        """测试设置测点值"""
        # 模拟响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": "200",
            "msg": "success",
            "data": None
        }
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        # 执行测试
        self.iot_api.set_value(device_id="dev1", point_id="V4", value="2")
        
        # 验证请求
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        self.assertEqual(call_args[1]['method'], 'POST')
        self.assertIn('/iot/open_api/v1/data/setValue', call_args[1]['url'])

class TestDeviceApi(unittest.TestCase):
    """测试设备管理 API"""
    
    def setUp(self):
        """设置测试环境"""
        self.client = TopStackClient(
            base_url="http://localhost:8000",
            api_key="test-api-key",
            project_id="test-project"
        )
        self.device_api = DeviceApi(self.client)
    
    @patch('topstack.client.requests.Session.request')
    def test_query_devices(self, mock_request):
        """测试查询设备"""
        # 模拟响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": "200",
            "msg": "success",
            "data": {
                "total": 1,
                "items": [
                    {
                        "id": "dev1",
                        "code": "DEV001",
                        "name": "测试设备",
                        "connectMode": "gateway",
                        "state": 0
                    }
                ]
            }
        }
        mock_response.ok = True
        mock_request.return_value = mock_response
        
        # 执行测试
        result = self.device_api.query(search="dev1", page_num=1, page_size=10)
        
        # 验证结果
        self.assertEqual(result.total, 1)
        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].id, "dev1")
        self.assertEqual(result.items[0].name, "测试设备")

if __name__ == '__main__':
    unittest.main() 